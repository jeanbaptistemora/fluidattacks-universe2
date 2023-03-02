# pylint: disable=too-many-lines
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
from aioextensions import (
    collect,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
)
import asyncio
import base64
import boto3
from context import (
    FI_AWS_REGION_NAME,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    InvalidRootComponent,
    RepeatedToeInput,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.findings.enums import (
    AttackComplexity,
    AttackVector,
    AvailabilityImpact,
    ConfidentialityImpact,
    Exploitability,
    FindingStateStatus,
    IntegrityImpact,
    PrivilegesRequired,
    RemediationLevel,
    ReportConfidence,
    SeverityScope,
    UserInteraction,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingMetadataToUpdate,
    SeverityScore,
)
from db_model.findings.update import (
    update_metadata as update_finding_metadata,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.get import (
    get_machine_executions_by_job_id,
)
from db_model.roots.types import (
    GitRoot,
    MachineFindingResult,
    RootMachineExecution,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.update import (
    update_historic_entry,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from findings import (
    domain as findings_domain,
)
from findings.domain.evidence import (
    update_evidence,
)
from findings.types import (
    FindingDraftToAdd,
)
from functools import (
    partial,
)
from io import (
    BytesIO,
)
import json
import logging
from newutils import (
    cvss as cvss_utils,
)
from newutils.files import (
    path_is_include,
)
from newutils.findings import (
    get_requirements_file,
    get_vulns_file,
)
from newutils.string import (
    boxify,
)
from newutils.vulnerabilities import (
    ignore_advisories,
    is_machine_vuln,
)
from organizations.utils import (
    get_organization,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
import os
import random
from roots.domain import (
    add_machine_execution,
)
from s3.resource import (
    get_s3_resource,
)
from signal import (
    SIGINT,
    signal,
    SIGTERM,
)
from starlette.datastructures import (
    UploadFile,
)
import tempfile
from tempfile import (
    SpooledTemporaryFile,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
)
from typing import (
    Any,
    NamedTuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from urllib.parse import (
    ParseResult,
    urlparse,
)
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.domain.snippet import (
    set_snippet,
)
from vulnerabilities.domain.utils import (
    get_hash,
    get_hash_from_typed,
    get_path_from_integrates_vulnerability,
)
from vulnerability_files.domain import (
    map_vulnerabilities_to_dynamo,
)
import yaml
from yaml.reader import (
    ReaderError,
)

logging.getLogger("boto").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("boto3").setLevel(logging.ERROR)

# Constants
LOGGER = logging.getLogger(__name__)
DUMMY_IMG: Image = Image.new("RGB", (0, 0))
DUMMY_DRAWING: ImageDraw = ImageDraw.Draw(DUMMY_IMG)
SNIPPETS_CONTEXT: int = 10
SNIPPETS_COLUMNS: int = 12 * SNIPPETS_CONTEXT


class Context(NamedTuple):
    loaders: Dataloaders
    headers: dict[str, str]


class SignalHandler:  # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.received_signal = False
        signal(SIGINT, self._signal_handler)  # type: ignore
        signal(SIGTERM, self._signal_handler)  # type: ignore

    def _signal_handler(self, _signal: str, _: Any) -> None:
        print(f"handling signal {_signal}, exiting gracefully")
        self.received_signal = True


async def get_config(
    execution_id: str,
    config_path: str | None = None,
) -> dict[str, Any]:
    # config_path is useful to test this flow locally
    if config_path is not None:
        with open(config_path, "rb") as config_file:
            return yaml.safe_load(config_file)
    s3_client = await get_s3_resource()
    print(f"configs/{execution_id}.yaml")
    with tempfile.NamedTemporaryFile() as temp:
        await s3_client.download_fileobj(
            "machine.data",
            f"configs/{execution_id}.yaml",
            temp,
        )

        temp.seek(0)
        return yaml.safe_load(temp)


@retry_on_exceptions(
    exceptions=(ClientPayloadError,),
    sleep_seconds=1,
)
async def get_sarif_log(
    execution_id: str,
    sarif_path: str | None = None,
) -> dict[str, Any] | None:
    # sarif_path is useful to test this flow locally
    if sarif_path is not None:
        with open(sarif_path, "rb") as sarif_file:
            return yaml.safe_load(sarif_file)
    s3_client = await get_s3_resource()
    with tempfile.NamedTemporaryFile() as temp:
        await s3_client.download_fileobj(
            "machine.data",
            f"results/{execution_id}.sarif",
            temp,
        )

        temp.seek(0)
        try:
            return yaml.safe_load(
                temp.read().decode(encoding="utf-8").replace("x0081", "")
            )
        except ReaderError:
            return None


def generate_cssv_vector(criteria_vulnerability: dict[str, Any]) -> str:
    score = criteria_vulnerability["score"]
    base = score["base"]
    temporal = score["temporal"]
    return (
        "CVSS:3.1"
        f"/AV:${base['attack_vector']}/AC:${base['attack_complexity']}"
        f"/PR:${base['privileges_required']}/UI:${base['user_interaction']}"
        f"/S:${base['scope']}/C:${base['confidentiality']}"
        f"/I:${base['integrity']}/A:${base['availability']}"
        f"/E:${temporal['exploit_code_maturity']}"
        f"/RL:${temporal['remediation_level']}"
        f"/RC:${temporal['report_confidence']}"
    )


def clarify_blocking(image: Image, ratio: float) -> Image:
    image_mask: Image = image.convert("L")
    image_mask_pixels = image_mask.load()

    image_width, image_height = image_mask.size

    for i in range(image_width):
        for j in range(image_height):
            if image_mask_pixels[i, j]:
                image_mask_pixels[i, j] = int(ratio * 0xFF)

    image.putalpha(image_mask)

    return image


async def to_png(*, string: str, margin: int = 25) -> UploadFile:
    font = ImageFont.truetype(
        font=os.environ["SKIMS_ROBOTO_FONT"],
        size=18,
    )
    watermark: Image = clarify_blocking(
        image=Image.open(os.environ["SKIMS_FLUID_WATERMARK"]),
        ratio=0.15,
    )
    # Make this image rectangular
    string = boxify(string=string)

    # This is the number of pixes needed to draw this text, may be big
    size: tuple[int, int] = DUMMY_DRAWING.textsize(string, font=font)
    size = (
        size[0] + 2 * margin,
        size[1] + 2 * margin,
    )
    watermark_size: tuple[int, int] = (
        size[0] // 2,
        watermark.size[1] * size[0] // watermark.size[0] // 2,
    )
    watermark_position: tuple[int, int] = (
        (size[0] - watermark_size[0]) // 2,
        (size[1] - watermark_size[1]) // 2,
    )

    # Create an image with the right size to fit the snippet
    #  and resize it to a common resolution
    img: Image = Image.new("RGB", size, (0xFF, 0xFF, 0xFF))

    drawing: ImageDraw = ImageDraw.Draw(img)
    drawing.multiline_text(
        xy=(margin, margin),
        text=string,
        fill=(0x33, 0x33, 0x33),
        font=font,
    )

    watermark = watermark.resize(watermark_size)
    img.paste(watermark, watermark_position, watermark)

    stream: BytesIO = BytesIO()

    img.save(stream, format="PNG")

    stream.seek(0)

    file_object = UploadFile(
        filename="evidence",
        content_type="image/png",
        # pylint: disable-next=consider-using-with
        file=SpooledTemporaryFile(mode="wb"),  # type: ignore
    )
    await file_object.write(stream.read())
    await file_object.seek(0)
    return file_object


def _get_finding_severity(
    criteria_vulnerability: dict[str, Any],
) -> Finding31Severity:
    return Finding31Severity(
        attack_complexity=AttackComplexity[
            criteria_vulnerability["score"]["base"]["attack_complexity"]
        ].value,
        attack_vector=AttackVector[
            criteria_vulnerability["score"]["base"]["attack_vector"]
        ].value,
        availability_impact=AvailabilityImpact[
            criteria_vulnerability["score"]["base"]["availability"]
        ].value,
        confidentiality_impact=ConfidentialityImpact[
            criteria_vulnerability["score"]["base"]["confidentiality"]
        ].value,
        exploitability=Exploitability[
            criteria_vulnerability["score"]["temporal"][
                "exploit_code_maturity"
            ]
        ].value,
        integrity_impact=IntegrityImpact[
            criteria_vulnerability["score"]["base"]["integrity"]
        ].value,
        privileges_required=PrivilegesRequired[
            criteria_vulnerability["score"]["base"]["privileges_required"]
        ].value,
        remediation_level=RemediationLevel[
            criteria_vulnerability["score"]["temporal"]["remediation_level"]
        ].value,
        report_confidence=ReportConfidence[
            criteria_vulnerability["score"]["temporal"]["report_confidence"]
        ].value,
        severity_scope=SeverityScope[
            criteria_vulnerability["score"]["base"]["scope"]
        ].value,
        user_interaction=UserInteraction[
            criteria_vulnerability["score"]["base"]["user_interaction"]
        ].value,
    )


async def _update_finding_metadata(
    finding_data: tuple[str, str, str],
    finding: Finding,
    criteria_vulnerability: dict[str, Any],
    criteria_requirements: dict[str, Any],
) -> None:
    group_name, vulnerability_id, language = finding_data
    language = language.lower()
    current_attrs = FindingMetadataToUpdate(
        attack_vector_description=finding.attack_vector_description,
        description=finding.description,
        min_time_to_remediate=finding.min_time_to_remediate,
        recommendation=finding.recommendation,
        requirements=finding.requirements,
        severity=finding.severity,
        threat=finding.threat,
        title=finding.title,
    )
    new_severity = _get_finding_severity(criteria_vulnerability)

    updated_attrs = FindingMetadataToUpdate(
        attack_vector_description=criteria_vulnerability[language]["impact"],
        description=criteria_vulnerability[language]["description"],
        min_time_to_remediate=int(criteria_vulnerability["remediation_time"]),
        recommendation=criteria_vulnerability[language]["recommendation"],
        requirements="\n".join(
            [
                criteria_requirements[item][language]["title"]
                for item in criteria_vulnerability["requirements"]
            ]
        ),
        severity=new_severity,
        severity_score=SeverityScore(
            base_score=cvss_utils.get_severity_base_score(new_severity),
            temporal_score=cvss_utils.get_severity_temporal_score(
                new_severity
            ),
            cvssf=cvss_utils.get_cvssf_score(
                cvss_utils.get_severity_temporal_score(new_severity)
            ),
        ),
        threat=criteria_vulnerability[language]["threat"],
        title=(
            f"{vulnerability_id}. "
            f"{criteria_vulnerability[language]['title']}"
        ),
    )

    if current_attrs != updated_attrs:
        await update_finding_metadata(
            group_name=group_name,
            finding_id=finding.id,
            metadata=updated_attrs,
        )


async def _create_draft(  # pylint: disable = too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    vulnerability_id: str,
    language: str,
    criteria_vulnerability: dict[str, Any],
    criteria_requirements: dict[str, Any],
) -> Finding:
    language = language.lower()
    severity_info = _get_finding_severity(criteria_vulnerability)

    draft_info = FindingDraftToAdd(
        attack_vector_description=criteria_vulnerability[language]["impact"],
        description=criteria_vulnerability[language]["description"],
        hacker_email="machine@fluidattacks.com",
        min_time_to_remediate=criteria_vulnerability["remediation_time"],
        recommendation=criteria_vulnerability[language]["recommendation"],
        requirements="\n".join(
            [
                criteria_requirements[item][language]["title"]
                for item in criteria_vulnerability["requirements"]
            ]
        ),
        severity=severity_info,
        threat=criteria_vulnerability[language]["threat"],
        title=(
            f"{vulnerability_id}. "
            f"{criteria_vulnerability[language]['title']}"
        ),
    )

    return await findings_domain.add_draft(
        loaders,
        group_name,
        "machine@fluidattacks.com",
        draft_info,
        source=Source.MACHINE,
    )


def _get_path_from_sarif_vulnerability(
    vulnerability: dict[str, Any], ignore_cve: bool = False
) -> str:
    if vulnerability["properties"]["kind"] == "inputs":
        what = _get_input_url(vulnerability)
    else:
        what = vulnerability["locations"][0]["physicalLocation"][
            "artifactLocation"
        ]["uri"]

    if (
        (properties := vulnerability.get("properties"))
        and (technique_value := properties.get("technique"))
        and (technique_value == "SCA")
        and (message_properties := vulnerability["message"].get("properties"))
    ):
        what = " ".join(
            (
                what,
                (
                    f"({message_properties['dependency_name']} "
                    f"v{message_properties['dependency_version']})"
                ),
                f"[{', '.join(message_properties['cve'])}]",
            )
        )

    if (
        (properties := vulnerability.get("properties"))
        and (
            properties.get("source_method")
            == "python.pip_incomplete_dependencies_list"
        )
        and (message_properties := vulnerability["message"].get("properties"))
        and (vulnerability["ruleId"] == "120")
    ):
        what = " ".join(
            (
                what,
                (
                    "(missing dependency: "
                    f"{message_properties['dependency_name']})"
                ),
            )
        )
    if ignore_cve:
        what = ignore_advisories(what)

    return what


def _get_vulns_with_reattack(  # NOSONAR
    stream: dict[str, Any],
    integrates_vulnerabilities: tuple[Vulnerability, ...],
    state: str,
) -> tuple[Vulnerability, ...]:
    result: tuple[Vulnerability, ...] = ()
    for vulnerability in integrates_vulnerabilities:
        if not (
            vulnerability.verification
            and vulnerability.verification.status
            == VulnerabilityVerificationStatus.REQUESTED
        ):
            continue
        for _vuln in stream["lines"]:
            if _vuln["state"] == state and _vuln["hash"] == vulnerability.hash:
                result = (*result, vulnerability)
                break
        for _vuln in stream["inputs"]:
            if _vuln["state"] == state and _vuln["hash"] == vulnerability.hash:
                result = (*result, vulnerability)
                break

    return result


def _get_input_url(
    vuln: dict[str, Any], repo_nickname: str | None = None
) -> str:
    url: str
    if vuln["properties"].get("has_redirect", False):
        url = vuln["properties"]["original_url"]
    else:
        url = vuln["locations"][0]["physicalLocation"]["artifactLocation"][
            "uri"
        ]
    while url.endswith("/"):
        url = url.rstrip("/")

    if repo_nickname:
        return f"{url} ({repo_nickname})"
    return url


def _build_vulnerabilities_stream_from_sarif(
    vulnerabilities: list[dict[str, Any]],
    commit_hash: str,
    repo_nickname: str,
) -> dict[str, Any]:
    return {
        "inputs": [
            {
                "field": f"{vuln['locations'][0]['physicalLocation']['region']['startLine']}",  # noqa: E501 pylint: disable=line-too-long
                "repo_nickname": repo_nickname,
                "state": "open",
                "stream": vuln["properties"]["stream"],
                "url": _get_input_url(vuln, repo_nickname),
                "skims_method": vuln["properties"]["source_method"],
                "skims_technique": vuln["properties"]["technique"],
                "developer": vuln["properties"]["method_developer"],
                "source": "MACHINE",
                "hash": vuln.get("guid", 0),
            }
            for vuln in vulnerabilities
            if vuln["properties"]["kind"] == "inputs"
        ],
        "lines": [
            {
                "commit_hash": commit_hash,
                "line": str(
                    vuln["locations"][0]["physicalLocation"]["region"][
                        "startLine"
                    ]
                ),
                "path": _get_path_from_sarif_vulnerability(vuln),
                "repo_nickname": repo_nickname,
                "state": "open",
                "skims_method": vuln["properties"]["source_method"],
                "skims_technique": vuln["properties"]["technique"],
                "developer": vuln["properties"]["method_developer"],
                "source": "MACHINE",
                "hash": vuln.get("guid", 0),
            }
            for vuln in vulnerabilities
            if vuln["properties"]["kind"] == "lines"
        ],
    }


def _build_vulnerabilities_stream_from_integrates(
    vulnerabilities: tuple[Vulnerability, ...],
    git_root: GitRoot,
    state: str | None = None,
    commit: str | None = None,
) -> dict[str, Any]:
    state = state or "closed"
    return {
        "inputs": [
            {
                "field": vuln.state.specific,  # noqa
                "repo_nickname": git_root.state.nickname,
                "state": state,
                "stream": ",".join(vuln.stream or []),
                "url": vuln.state.where,
                "skims_method": vuln.skims_method,
                "skims_technique": vuln.skims_technique,
                "developer": vuln.developer,
                "source": vuln.state.source.value,
                "hash": vuln.hash,
            }
            for vuln in vulnerabilities
            if vuln.type == VulnerabilityType.INPUTS
        ],
        "lines": [
            {
                "commit_hash": commit or vuln.state.commit,
                "line": vuln.state.specific,
                "path": vuln.state.where,
                "repo_nickname": git_root.state.nickname,
                "state": state,
                "skims_method": vuln.skims_method,
                "skims_technique": vuln.skims_technique,
                "developer": vuln.developer,
                "source": vuln.state.source.value,
                "hash": vuln.hash,
            }
            for vuln in vulnerabilities
            if vuln.type == VulnerabilityType.LINES
        ],
    }


def _machine_vulns_to_close(
    sarif_vulns: list[dict[str, Any]],
    existing_open_machine_vulns: tuple[Vulnerability, ...],
    execution_config: dict[str, Any],
) -> tuple[Vulnerability, ...]:
    sarif_hashes: set[int] = {vuln["guid"] for vuln in sarif_vulns}

    return tuple(
        vuln
        for vuln in existing_open_machine_vulns
        # his result was not found by Skims
        if vuln.hash
        and vuln.hash not in sarif_hashes
        and (
            # the result path is included in the current analysis
            path_is_include(
                (
                    get_path_from_integrates_vulnerability(
                        vuln.state.where,
                        vuln.type,
                        ignore_cve=vuln.type == VulnerabilityType.LINES,
                    )[1]
                ).split(" ", maxsplit=1)[0],
                [
                    *(execution_config["path"]["include"]),
                    *(execution_config["apk"]["include"]),
                ],
                [
                    *(execution_config["path"]["exclude"]),
                    *(execution_config["apk"]["exclude"]),
                ],
            )
            if vuln.type == VulnerabilityType.LINES
            else (
                execution_config.get("dast")
                if vuln.type == VulnerabilityType.INPUTS
                else True
            )
        )
    )


async def ensure_toe_inputs(
    loaders: Dataloaders, group_name: str, root_id: str, stream: dict[str, Any]
) -> None:
    vulns_for_toe: list[dict[str, Any]] = [
        vuln
        for vuln in stream["inputs"]
        if vuln["state"] == "open" and vuln["skims_technique"] != "APK"
    ]
    if vulns_for_toe:
        parsed_toes: list[ParseResult] = [
            parsed_url
            for vuln in vulns_for_toe
            if (parsed_url := urlparse(vuln["url"].split(" ")[0]))
        ]

        for vuln in vulns_for_toe:
            url: str = vuln["url"].split(" ")[0]
            parsed_url = urlparse(url)
            with suppress(RepeatedToeInput):
                try:
                    await toe_inputs_domain.add(
                        loaders=loaders,
                        group_name=group_name,
                        component=url,
                        entry_point="",
                        attributes=ToeInputAttributesToAdd(
                            be_present=True,
                            unreliable_root_id=root_id,
                            has_vulnerabilities=False,
                            seen_first_time_by="machine@fluidattacks.com",
                        ),
                    )
                except InvalidRootComponent as exc:
                    # Some invalid component may be the same domain
                    # as a valid component with different scheme,
                    # since Machine analyzes both the HTTP and HTTPS urls.
                    # There is no need to break the execution
                    # if that is the case
                    if (
                        len(
                            [
                                toe
                                for toe in parsed_toes
                                if (
                                    toe.scheme != parsed_url.scheme
                                    and toe.netloc == parsed_url.netloc
                                )
                            ]
                        )
                        == 0
                    ):
                        raise exc


async def persist_vulnerabilities(
    *,
    loaders: Dataloaders,
    group_name: str,
    git_root: GitRoot,
    finding: Finding,
    stream: dict[str, Any],
    organization_name: str,
) -> set[str] | None:
    finding_policy = await policies_domain.get_finding_policy_by_name(
        loaders=loaders,
        organization_name=organization_name,
        finding_name=finding.title.lower(),
    )

    if (len(stream["inputs"]) + len(stream["lines"])) > 0:
        length = len(stream["inputs"]) + len(stream["lines"])
        LOGGER.info(
            "%s vulns to modify for the finding %s", length, finding.id
        )
        await ensure_toe_inputs(loaders, group_name, git_root.id, stream)
        loaders.toe_input.clear_all()
        result = await map_vulnerabilities_to_dynamo(
            loaders=loaders,
            vulns_data_from_file=stream,
            group_name=group_name,
            finding_id=finding.id,
            finding_policy=finding_policy,
            user_info={
                "user_email": "machine@fluidattacks.com",
                "first_name": "Machine",
                "last_name": "Services",
            },
            raise_validation=False,
        )

        loaders.finding.clear(finding.id)
        loaders.finding_vulnerabilities.clear(finding.id)
        return result
    return None


async def upload_evidences(
    loaders: Dataloaders,
    finding: Finding,
    machine_vulnerabilities: list[dict[str, Any]],
) -> bool:
    success: bool = True
    evidence_ids = [("evidence_route_5", "evidence_route_5")]
    number_of_samples: int = min(
        len(machine_vulnerabilities), len(evidence_ids)
    )
    result_samples: tuple[dict[str, Any], ...] = tuple(
        random.sample(machine_vulnerabilities, k=number_of_samples),
    )
    evidence_descriptions = [
        result["message"]["text"] for result in result_samples
    ]
    evidence_streams: tuple[UploadFile, ...] = tuple()
    for result in result_samples:
        evidence_streams = (
            *evidence_streams,
            await to_png(
                string=result["locations"][0]["physicalLocation"]["region"][
                    "snippet"
                ]["text"]
            ),
        )
    for (evidence_id, _), evidence_stream, evidence_description in zip(
        evidence_ids, evidence_streams, evidence_descriptions
    ):
        # Exception may happen
        # due to two reports trying to update the evidence concurrently
        # or trying to upload the same evidence
        with suppress(ConditionalCheckFailedException):
            await update_evidence(
                loaders,
                finding.id,
                evidence_id,
                evidence_stream,
                description=evidence_description,
            )

    loaders.finding.clear(finding.id)
    return success


async def release_finding(
    loaders: Dataloaders, finding_id: str, auto_approve: bool = False
) -> None:
    finding = await findings_domain.get_finding(loaders, finding_id)
    if finding.approval and (
        finding.approval.status == FindingStateStatus.APPROVED
    ):
        return

    # Several process may try to submit the same finding concurrently.
    # Handle the exception in case one already did it
    with suppress(AlreadySubmitted):
        await findings_domain.submit_draft(
            loaders, finding_id, "machine@fluidattacks.com", Source.MACHINE
        )

    if auto_approve:
        loaders.finding.clear(finding.id)

        # Ensure that submission and approval date are not the same
        # For analytics purposes
        await asyncio.sleep(2)

        # Several process may try to approve the same finding concurrently.
        # Handle the exception in case one already did it
        with suppress(AlreadyApproved):
            await findings_domain.approve_draft(
                loaders, finding_id, "machine@fluidattacks.com", Source.MACHINE
            )


def _filter_vulns_already_reported(
    sarif_vulns: dict[str, Any],
    existing_open_machine_vulns: tuple[Vulnerability, ...],
) -> Any:
    vulns_already_reported = {
        vuln.hash
        for vuln in existing_open_machine_vulns
        if (
            vuln.verification is None
            or (
                vuln.verification.status
                != VulnerabilityVerificationStatus.REQUESTED
            )
        )
    }
    return {
        "inputs": [
            vuln
            for vuln in sarif_vulns["inputs"]
            if vuln["hash"] not in vulns_already_reported
        ],
        "lines": [
            vuln
            for vuln in sarif_vulns["lines"]
            if vuln["hash"] not in vulns_already_reported
        ],
    }


async def update_vulns_already_reported(
    sarif_vulns: dict[str, Any],
    existing_open_machine_vulns: tuple[Vulnerability, ...],
) -> None:
    """Some field of the vulnerability can change, but it is still the same
    vulnerability, the status of the vulnerability must be updated.
    """
    vulns_already_reported = {
        vuln.hash: vuln
        for vuln in existing_open_machine_vulns
        if (
            vuln.verification is None
            or (
                vuln.verification.status
                != VulnerabilityVerificationStatus.REQUESTED
            )
        )
        and vuln.hash
    }
    futures = []
    for vuln in sarif_vulns["lines"]:
        if (_current_vuln := vulns_already_reported.get(vuln["hash"])) and (
            vuln["path"] != _current_vuln.state.where
        ):
            new_state = _current_vuln.state._replace(
                where=vuln["path"],
                modified_date=datetime.utcnow(),
                source=Source.MACHINE,
                modified_by="machine@fluidattacks.com",
                commit=vuln["commit_hash"],
            )
            futures.append(
                update_historic_entry(
                    current_value=_current_vuln,
                    finding_id=_current_vuln.finding_id,
                    entry=new_state,
                    vulnerability_id=_current_vuln.id,
                )
            )
    await collect(futures, workers=50)


async def _is_machine_finding(loaders: Dataloaders, finding_id: str) -> bool:
    is_machine_finding: bool = False
    historic_state = await loaders.finding_historic_state.load(finding_id)
    for state in reversed(historic_state):
        if state.status == FindingStateStatus.CREATED:
            is_machine_finding = state.source == Source.MACHINE
            break

    return is_machine_finding


async def upload_snippet(
    loaders: Dataloaders,
    root: GitRoot,
    vuln_id: str,
    sarif_vulns: list[Any],
) -> None:
    current_vuln = await vulns_domain.get_vulnerability(loaders, vuln_id)
    if current_vuln.state.status != VulnerabilityStateStatus.VULNERABLE:
        return

    current_hash = get_hash_from_typed(current_vuln)
    for vuln in sarif_vulns:
        if vuln["properties"]["kind"] == "lines":
            _hash = get_hash(
                vuln["locations"][0]["physicalLocation"]["region"][
                    "startLine"
                ],
                "LINES",
                ignore_advisories(
                    _get_path_from_sarif_vulnerability(vuln, False)
                ),
                current_vuln.root_id,
            )
        else:
            _hash = get_hash(
                vuln["locations"][0]["physicalLocation"]["region"][
                    "startLine"
                ],
                "INPUTS",
                ignore_advisories(_get_input_url(vuln, root.state.nickname)),
                current_vuln.root_id,
            )
        if current_hash == _hash:
            await set_snippet(
                current_vuln,
                current_vuln.state,
                vuln["locations"][0]["physicalLocation"]["region"]["snippet"][
                    "text"
                ],
            )
            break


def _has_machine_description(
    finding: Finding, criteria_vulnerability: dict[str, Any], language: str
) -> bool:
    return all(
        (
            finding.description.strip()
            == criteria_vulnerability[language]["description"].strip(),
            finding.threat.strip()
            == criteria_vulnerability[language]["threat"].strip(),
            finding.severity == _get_finding_severity(criteria_vulnerability),
        )
    )


async def _split_target_findings(
    criteria_vulnerability: dict[str, Any],
    language: str,
    same_type_of_findings: tuple[Finding, ...],
) -> tuple[Finding | None, tuple[Finding, ...]]:
    target_finding = None
    non_target_findings: list[Finding] = []
    for finding in same_type_of_findings:
        if _has_machine_description(finding, criteria_vulnerability, language):
            target_finding = finding
        else:
            non_target_findings.append(finding)
    return target_finding, tuple(non_target_findings)


async def _close_vulns_in_non_target(  # pylint: disable = too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    git_root: GitRoot,
    sarif_log: dict[str, Any],
    execution_config: dict[str, Any],
    organization_name: str,
    sarif_vulns: list,
    finding: Finding,
) -> None:
    existing_open_machine_vulns = tuple(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding.id)
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
        and is_machine_vuln(vuln)
        and vuln.root_id == git_root.id
    )
    existing_vulns_to_close = _build_vulnerabilities_stream_from_integrates(
        _machine_vulns_to_close(
            sarif_vulns,
            existing_open_machine_vulns,
            execution_config,
        ),
        git_root,
        state="closed",
        commit=sarif_log["runs"][0]["versionControlProvenance"][0][
            "revisionId"
        ],
    )
    if persisted_vulns := await persist_vulnerabilities(
        loaders=loaders,
        group_name=group_name,
        git_root=git_root,
        finding=finding,
        stream={
            "inputs": [
                *existing_vulns_to_close["inputs"],
            ],
            "lines": [
                *existing_vulns_to_close["lines"],
            ],
        },
        organization_name=organization_name,
    ):
        await update_unreliable_indicators_by_deps(
            EntityDependency.upload_file,
            finding_ids=[finding.id],
            vulnerability_ids=list(persisted_vulns),
        )


async def process_criteria_vuln(  # pylint: disable=too-many-locals
    *,
    loaders: Dataloaders,
    group_name: str,
    vulnerability_id: str,
    criteria_vulnerability: dict[str, Any],
    criteria_requirements: dict[str, Any],
    language: str,
    git_root: GitRoot,
    sarif_log: dict[str, Any],
    execution_config: dict[str, Any],
    organization_name: str,
    finding: Finding | None = None,
    auto_approve: bool = False,
) -> MachineFindingResult | None:
    sarif_vulns = [
        vuln
        for vuln in sarif_log["runs"][0]["results"]
        if vuln["ruleId"] == vulnerability_id
    ]

    if len(sarif_vulns) > 0:
        if finding is None:
            finding = await _create_draft(
                loaders,
                group_name,
                vulnerability_id,
                language,
                criteria_vulnerability,
                criteria_requirements,
            )
            loaders.group_findings.clear(group_name)
        else:
            await _update_finding_metadata(
                (group_name, vulnerability_id, language),
                finding,
                criteria_vulnerability,
                criteria_requirements,
            )

    if not finding:
        return None

    existing_open_machine_vulns: tuple[Vulnerability, ...] = tuple(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding.id)
        if vuln.state.status == VulnerabilityStateStatus.VULNERABLE
        and is_machine_vuln(vuln)
        and vuln.root_id == git_root.id
    )

    existing_vulns_to_close = _build_vulnerabilities_stream_from_integrates(
        _machine_vulns_to_close(
            sarif_vulns,
            existing_open_machine_vulns,
            execution_config,
        ),
        git_root,
        state="closed",
        commit=sarif_log["runs"][0]["versionControlProvenance"][0][
            "revisionId"
        ],
    )
    new_vulns_to_add = _filter_vulns_already_reported(
        _build_vulnerabilities_stream_from_sarif(
            sarif_vulns,
            sarif_log["runs"][0]["versionControlProvenance"][0]["revisionId"],
            git_root.state.nickname,
        ),
        existing_open_machine_vulns,
    )

    reattack_future = findings_domain.add_reattack_justification(
        loaders,
        finding.id,
        _get_vulns_with_reattack(
            new_vulns_to_add, existing_open_machine_vulns, "open"
        ),
        _get_vulns_with_reattack(
            existing_vulns_to_close, existing_open_machine_vulns, "closed"
        ),
        sarif_log["runs"][0]["versionControlProvenance"][0]["revisionId"],
        CommentType.VERIFICATION,
    )

    should_update_evidence: bool = False
    await update_vulns_already_reported(
        _build_vulnerabilities_stream_from_sarif(
            sarif_vulns,
            sarif_log["runs"][0]["versionControlProvenance"][0]["revisionId"],
            git_root.state.nickname,
        ),
        existing_open_machine_vulns,
    )
    if persisted_vulns := await persist_vulnerabilities(
        loaders=loaders,
        group_name=group_name,
        git_root=git_root,
        finding=finding,
        stream={
            "inputs": [
                *new_vulns_to_add["inputs"],
                *existing_vulns_to_close["inputs"],
            ],
            "lines": [
                *new_vulns_to_add["lines"],
                *existing_vulns_to_close["lines"],
            ],
        },
        organization_name=organization_name,
    ):
        should_update_evidence = True
        await reattack_future
        # Update all finding indicators with latest information
        await update_unreliable_indicators_by_deps(
            EntityDependency.upload_file,
            finding_ids=[finding.id],
            vulnerability_ids=list(persisted_vulns),
        )
    else:
        reattack_future.close()

    if should_update_evidence or (
        finding.evidences.evidence5 is None and len(sarif_vulns) > 0
    ):
        await upload_evidences(loaders, finding, sarif_vulns)

    if await _is_machine_finding(loaders, finding.id) and (
        len(new_vulns_to_add) > 0 or len(existing_open_machine_vulns) > 0
    ):
        await release_finding(loaders, finding.id, auto_approve)
    return MachineFindingResult(
        open=len(new_vulns_to_add["lines"]) + len(new_vulns_to_add["inputs"]),
        modified=len(existing_vulns_to_close["inputs"])
        + len(existing_vulns_to_close["lines"]),
        finding=f"F{vulnerability_id}",
    )


async def get_current_execution(
    root_id: str,
    batch_job_id: str,
    findings_executed: list[MachineFindingResult] | None = None,
    commit: str | None = None,
) -> RootMachineExecution | None:

    result = await get_machine_executions_by_job_id(
        job_id=batch_job_id, root_id=root_id
    )
    if not result:
        if await add_machine_execution(
            root_id,
            batch_job_id,
            findings_executed=findings_executed or [],
            commit=commit,
        ):
            with suppress(IndexError):
                return (
                    await get_machine_executions_by_job_id(
                        job_id=batch_job_id, root_id=root_id
                    )
                )[0]
        return None
    return result[0]


async def process_execution(
    execution_id: str,
    criteria_vulns: dict[str, Any] | None = None,
    criteria_reqs: dict[str, Any] | None = None,
    config_path: str | None = None,
    sarif_path: str | None = None,
) -> bool:
    # pylint: disable=too-many-locals
    criteria_vulns = criteria_vulns or await get_vulns_file()
    criteria_reqs = criteria_reqs or await get_requirements_file()
    loaders: Dataloaders = get_new_context()
    group_name = execution_id.split("_", maxsplit=1)[0]
    execution_config = await get_config(execution_id, config_path)
    try:
        git_root = next(
            root
            for root in await loaders.group_roots.load(group_name)
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
            and root.state.nickname == execution_config["namespace"]
        )
    except StopIteration:
        LOGGER.warning(
            "Cloud not find root for the execution",
            extra={
                "extra": {
                    "execution_id": execution_id,
                    "nickname": execution_config["namespace"],
                }
            },
        )
        return False
    results = await get_sarif_log(execution_id, sarif_path)
    if not results:
        LOGGER.warning(
            "Could not find execution result",
            extra={"extra": {"execution_id": execution_id}},
        )
        return False

    rules_id: set[str] = {
        item["id"] for item in results["runs"][0]["tool"]["driver"]["rules"]
    }
    if not rules_id:
        return True
    auto_approve_rules: dict[str, bool] = {
        item["id"]: item.get("properties", {}).get("auto_approve", False)
        for item in results["runs"][0]["tool"]["driver"]["rules"]
    }

    group_findings = await loaders.group_drafts_and_findings.load(group_name)
    rules_finding: tuple[tuple[str, Finding | None], ...] = ()
    for criteria_vuln_id in rules_id:
        for finding in group_findings:
            if finding.title.startswith(f"{criteria_vuln_id}."):
                rules_finding = (*rules_finding, (criteria_vuln_id, finding))
                break
        else:
            rules_finding = (*rules_finding, (criteria_vuln_id, None))

    organization_name = (
        await get_organization(
            loaders, (await loaders.group.load(group_name)).organization_id
        )
    ).name
    await collect(
        [
            process_criteria_vuln(
                loaders=loaders,
                group_name=group_name,
                vulnerability_id=vuln_id,
                criteria_vulnerability=criteria_vulns[vuln_id],
                criteria_requirements=criteria_reqs,
                finding=finding,
                language=execution_config["language"],
                git_root=git_root,
                sarif_log=results,
                execution_config=execution_config,
                organization_name=organization_name,
                auto_approve=auto_approve_rules[vuln_id],
            )
            for vuln_id, finding in rules_finding
        ]
    )
    return True


def _decode_sqs_message(message: Any) -> str:
    with suppress(json.JSONDecodeError):
        return json.loads(message.body)["execution_id"]
    return json.loads(
        base64.b64decode(
            json.loads(base64.b64decode(message.body).decode())["body"]
        ).decode()
    )["id"]


def _delete_message(queue: Any, message: Any) -> None:
    queue.delete_messages(
        Entries=[
            {
                "Id": message.message_id,
                "ReceiptHandle": message.receipt_handle,
            },
        ]
    )


def _callback_done(
    future: asyncio.Future, *, message: Any, queue: Any
) -> None:
    if future.done():
        if exception := future.exception():
            message_id = _decode_sqs_message(message)
            LOGGER.error(
                "An error has occurred consuming a report",
                extra={
                    "extra": {
                        "execution_id": message_id,
                        "exception": str(exception),
                    }
                },
            )
        else:
            _delete_message(queue, message)


async def main() -> None:
    criteria_vulns = await get_vulns_file()
    criteria_reqs = await get_requirements_file()
    sqs = boto3.resource("sqs", region_name=FI_AWS_REGION_NAME)
    queue = sqs.get_queue_by_name(QueueName="skims-report-queue")
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        while len(asyncio.all_tasks()) > 10:
            await asyncio.sleep(0.3)

        messages = queue.receive_messages(
            MessageAttributeNames=[],
            MaxNumberOfMessages=10,
            VisibilityTimeout=600,
        )
        if not messages:
            messages = queue.receive_messages(
                MessageAttributeNames=[],
                MaxNumberOfMessages=10,
                VisibilityTimeout=600,
                WaitTimeSeconds=20,
            )
            if not messages:
                break

        for message in messages:
            task = asyncio.create_task(
                process_execution(
                    _decode_sqs_message(message),
                    criteria_vulns,
                    criteria_reqs,
                )
            )
            task.add_done_callback(
                partial(_callback_done, message=message, queue=queue)
            )
