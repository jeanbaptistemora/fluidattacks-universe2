from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
import aioboto3
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
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.enums import (
    Source,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from finding_comments import (
    domain as comments_domain,
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
    datetime as datetime_utils,
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
from organizations_finding_policies import (
    domain as policies_domain,
)
import os
import pytz  # type: ignore
import random
from settings.various import (
    TIME_ZONE,
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
from time import (
    time,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)
from vulnerability_files.domain import (
    map_vulnerabilities_to_dynamo,
)
import yaml  # type: ignore
from yaml.reader import (  # type: ignore
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


class SignalHandler:  # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.received_signal = False
        signal(SIGINT, self._signal_handler)  # type: ignore
        signal(SIGTERM, self._signal_handler)  # type: ignore

    def _signal_handler(self, _signal: str, _: Any) -> None:
        print(f"handling signal {_signal}, exiting gracefully")
        self.received_signal = True


async def get_config(
    boto3_session: aioboto3.Session, execution_id: str
) -> Dict[str, Any]:
    async with boto3_session.client("s3") as s3_client:
        with tempfile.NamedTemporaryFile() as temp:
            await s3_client.download_fileobj(
                "skims.data",
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
    boto3_session: aioboto3.Session,
    execution_id: str,
) -> Optional[Dict[str, Any]]:
    async with boto3_session.client("s3") as s3_client:
        with tempfile.NamedTemporaryFile() as temp:
            await s3_client.download_fileobj(
                "skims.data",
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


def generate_cssv_vector(criteria_vulnerability: Dict[str, Any]) -> str:
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
    size: Tuple[int, int] = DUMMY_DRAWING.textsize(string, font=font)
    size = (
        size[0] + 2 * margin,
        size[1] + 2 * margin,
    )
    watermark_size: Tuple[int, int] = (
        size[0] // 2,
        watermark.size[1] * size[0] // watermark.size[0] // 2,
    )
    watermark_position: Tuple[int, int] = (
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

    file = UploadFile(
        filename="evidence",
        content_type="image/png",
        file=SpooledTemporaryFile(  # pylint: disable=consider-using-with
            mode="wb"
        ),
    )
    await file.write(stream.read())
    await file.seek(0)
    return file


async def _create_draft(
    group_name: str,
    vulnerability_id: str,
    language: str,
    criteria_vulnerability: Dict[str, Any],
    criteria_requirements: Dict[str, Any],
) -> Finding:
    language = language.lower()
    severity_info = Finding31Severity(
        attack_complexity=Decimal("0.0"),
        attack_vector=Decimal("0.0"),
        availability_impact=Decimal("0.0"),
        confidentiality_impact=Decimal("0.0"),
        exploitability=Decimal("0.0"),
        integrity_impact=Decimal("0.0"),
        privileges_required=Decimal("0.0"),
        remediation_level=Decimal("0.0"),
        report_confidence=Decimal("0.0"),
        severity_scope=Decimal("0.0"),
        user_interaction=Decimal("0.0"),
    )
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
        group_name,
        "machine@fluidattacks.com",
        draft_info,
        source=Source.MACHINE,
    )


def _get_path_from_integrates_vulnerability(
    vulnerability: Vulnerability,
) -> Tuple[str, str]:
    if vulnerability.type in {
        VulnerabilityType.INPUTS,
        VulnerabilityType.PORTS,
    }:
        if len(chunks := vulnerability.where.rsplit(" (", maxsplit=1)) == 2:
            what, namespace = chunks
            namespace = namespace[:-1]
        else:
            what, namespace = chunks[0], ""
    elif vulnerability.type == VulnerabilityType.LINES:
        if len(chunks := vulnerability.where.split("/", maxsplit=1)) == 2:
            namespace, what = chunks
        else:
            namespace, what = "", chunks[0]
    else:
        raise NotImplementedError()

    return namespace, what


def _get_path_from_sarif_vulnerability(vulnerability: Dict[str, Any]) -> str:
    what = vulnerability["locations"][0]["physicalLocation"][
        "artifactLocation"
    ]["uri"]
    if (
        (properties := vulnerability.get("properties"))
        and (technique_value := properties.get("technique"))
        and (technique_value == "SCA")
        and (message_properties := vulnerability["message"].get("properties"))
        and (message_properties)
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

    return what


def _filter_vulns_to_open(
    stream: dict[str, Any],
    integrates_vulnerabilities: Tuple[Vulnerability, ...],
) -> dict[str, Any]:
    integrates_hashes = {
        hash((vuln.where, vuln.specific))
        for vuln in integrates_vulnerabilities
    }
    return {
        "inputs": [
            vuln
            for vuln in stream["inputs"]
            if hash((vuln["url"], vuln["field"])) not in integrates_hashes
        ],
        "lines": [
            vuln
            for vuln in stream["lines"]
            if hash((vuln["path"], vuln["line"])) not in integrates_hashes
        ],
    }


def _get_vulns_with_reattack(
    stream: dict[str, Any],
    integrates_vulnerabilities: Tuple[Vulnerability, ...],
    state: str,
) -> Tuple[Vulnerability, ...]:
    result: Tuple[Vulnerability, ...] = ()
    for vulnerability in integrates_vulnerabilities:
        if not (
            vulnerability.verification
            and vulnerability.verification.status
            == VulnerabilityVerificationStatus.REQUESTED
        ):
            continue
        for _vuln in stream["lines"]:
            if _vuln["state"] == state and hash(
                (_vuln["path"], _vuln["line"])
            ) == hash((vulnerability.where, vulnerability.specific)):
                result = (*result, vulnerability)
                break
        for _vuln in stream["inputs"]:
            if _vuln["state"] == state and hash(
                (_vuln["path"], _vuln["line"])
            ) == hash((vulnerability.where, vulnerability.specific)):
                result = (*result, vulnerability)
                break

    return result


def _build_vulnerabilities_stream_from_sarif(
    vulnerabilities: List[Dict[str, Any]],
    commit_hash: str,
    repo_nickname: str,
) -> Dict[str, Any]:
    return {
        "inputs": [
            {
                "field": f"{vuln['locations'][0]['physicalLocation']['region']['startLine']}",  # noqa
                "repo_nickname": repo_nickname,
                "state": "open",
                "stream": vuln["properties"]["stream"],
                "url": (
                    f"{vuln['locations'][0]['physicalLocation']['artifactLocation']['uri']}"  # noqa
                    f" ({repo_nickname})"
                ),
                "skims_method": vuln["properties"]["source_method"],
                "skims_technique": vuln["properties"].get("technique"),
                "developer": "",
                "source": "MACHINE",
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
                "path": (
                    f"{repo_nickname}/"
                    f"{_get_path_from_sarif_vulnerability(vuln)}"
                ),
                "repo_nickname": repo_nickname,
                "state": "open",
                "skims_method": vuln["properties"]["source_method"],
                "skims_technique": vuln["properties"].get("technique", ""),
                "developer": "",
                "source": "MACHINE",
            }
            for vuln in vulnerabilities
            if vuln["properties"]["kind"] == "lines"
        ],
    }


def _build_vulnerabilities_stream_from_integrates(
    vulnerabilities: Tuple[Vulnerability, ...], state: Optional[str] = None
) -> Dict[str, Any]:
    state = state or "closed"
    return {
        "inputs": [
            {
                "field": vuln.specific,  # noqa
                "repo_nickname": _get_path_from_integrates_vulnerability(vuln)[
                    0
                ],
                "state": state,
                "stream": vuln.stream,
                "url": vuln.where,
                "skims_method": vuln.skims_method,
                "skims_technique": vuln.skims_technique,
                "developer": vuln.developer,
                "source": vuln.state.source.value,
            }
            for vuln in vulnerabilities
            if vuln.type == VulnerabilityType.INPUTS
        ],
        "lines": [
            {
                "commit_hash": vuln.commit,
                "line": vuln.specific,
                "path": vuln.where,
                "repo_nickname": _get_path_from_integrates_vulnerability(vuln)[
                    0
                ],
                "state": state,
                "skims_method": vuln.skims_method,
                "skims_technique": vuln.skims_technique,
                "developer": vuln.developer,
                "source": vuln.state.source.value,
            }
            for vuln in vulnerabilities
            if vuln.type == VulnerabilityType.LINES
        ],
    }


def _machine_vulns_to_close(
    machine_vulnerabilities: List[Dict[str, Any]],
    integrates_vulns: Tuple[Vulnerability, ...],
    execution_config: Dict[str, Any],
) -> Tuple[Vulnerability, ...]:
    machine_hashes = {
        hash(
            (
                _get_path_from_sarif_vulnerability(vuln),
                str(
                    vuln["locations"][0]["physicalLocation"]["region"][
                        "startLine"
                    ]
                ),
            )
        )
        for vuln in machine_vulnerabilities
    }

    return tuple(
        vuln
        for vuln in integrates_vulns
        # his result was not found by Skims
        if hash(
            (_get_path_from_integrates_vulnerability(vuln)[1], vuln.specific)
        )
        not in machine_hashes
        and (
            # the result path is included in the current analysis
            path_is_include(
                _get_path_from_integrates_vulnerability(vuln)[1].split(
                    " ", maxsplit=1
                )[0],
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
    for vuln in stream["inputs"]:
        if vuln["state"] != "open":
            continue
        with suppress(Exception):
            await toe_inputs_domain.add(
                loaders=loaders,
                group_name=group_name,
                component=vuln["url"],
                entry_point=vuln["field"],
                attributes=ToeInputAttributesToAdd(
                    be_present=True,
                    unreliable_root_id=root_id,
                    has_vulnerabilities=False,
                    seen_first_time_by="machine@fluidattacks.com",
                ),
            )


async def persist_vulnerabilities(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    git_root: GitRoot,
    finding: Finding,
    stream: dict[str, Any],
    organization: str,
) -> Optional[Set[str]]:
    finding_policy = await policies_domain.get_finding_policy_by_name(
        org_name=organization,
        finding_name=finding.title.lower(),
    )

    if (len(stream["inputs"]) + len(stream["lines"])) > 0:
        length = len(stream["inputs"]) + len(stream["lines"])
        LOGGER.info(
            "%s vulns to modify for the finding %s", length, finding.id
        )
        await ensure_toe_inputs(loaders, group_name, git_root.id, stream)
        result = await map_vulnerabilities_to_dynamo(
            loaders=loaders,
            vulns_data_from_file=stream,
            group_name=group_name,
            finding_id=finding.id,
            finding_policy=finding_policy,
            user_info={
                "user_email": "machine@fluidattacks.com",
                "first_name": "machine",
                "last_name": "machine",
            },
            raise_validation=False,
        )
        return result
    return None


async def add_reattack_justification(
    finding_id: str,
    open_vulnerabilities: Tuple[Vulnerability, ...],
    closed_vulnerabilities: Tuple[Vulnerability, ...],
    commit_hash: str,
) -> None:
    today = datetime.now(tz=timezone.utc)
    format_date = today.astimezone(tz=pytz.timezone(TIME_ZONE)).strftime(
        "%Y/%m/%d %H:%M"
    )
    open_justification: str = ""
    closed_justification: str = ""

    closed_vulns_strs = [
        f"  - {vuln.where}" for vuln in closed_vulnerabilities
    ]
    open_vulns_strs = [f"  - {vuln.where}" for vuln in open_vulnerabilities]
    str_open_vulns = "\n ".join(open_vulns_strs) if open_vulns_strs else ""
    str_closed_vulns = (
        "\n ".join(closed_vulns_strs) if closed_vulns_strs else ""
    )

    open_justification = (
        "Reported vulnerabilities are still open in commit "
        + f"{commit_hash}: \n {str_open_vulns}"
        if open_vulns_strs
        else ""
    )
    if open_justification:
        open_justification = (
            "A reattack request was executed on "
            + f"{format_date.replace(' ', ' at ')}.\n"
            + open_justification
        )
        await comments_domain.add(
            FindingComment(
                finding_id=finding_id,
                id=str(round(time() * 1000)),
                comment_type=CommentType.COMMENT,
                parent_id="0",
                creation_date=datetime_utils.get_as_utc_iso_format(
                    datetime_utils.get_now()
                ),
                full_name="machine",
                content=open_justification,
                email="machine@fluidttacks.com",
            )
        )
    closed_justification = (
        "Reattack request was executed on "
        + f"{format_date.replace(' ', ' at ')}. \n"
        + "Reported vulnerabilities were solved "
        + f"in commit {commit_hash}: \n"
        + f"{str_closed_vulns} \n"
        if closed_vulns_strs
        else ""
    )
    if closed_justification:
        await comments_domain.add(
            FindingComment(
                finding_id=finding_id,
                id=str(round(time() * 1000)),
                comment_type=CommentType.CONSULT,
                parent_id="0",
                creation_date=datetime_utils.get_as_utc_iso_format(
                    datetime_utils.get_now()
                ),
                full_name="machine",
                content=closed_justification,
                email="machine@fluidttacks.com",
            )
        )


async def upload_evidences(
    loaders: Dataloaders,
    finding: Finding,
    machine_vulnerabilities: list[dict[str, Any]],
) -> None:
    evidence_ids = [("evidence_route_5", "evidence_route_5")]
    number_of_samples: int = min(
        len(machine_vulnerabilities), len(evidence_ids)
    )
    result_samples: Tuple[dict[str, Any], ...] = tuple(
        random.sample(machine_vulnerabilities, k=number_of_samples),
    )
    evidence_descriptions = [
        result["message"]["text"] for result in result_samples
    ]
    evidence_streams: Tuple[UploadFile, ...] = tuple()
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
        try:
            await update_evidence(
                loaders,
                finding.id,
                evidence_id,
                evidence_stream,
                description=evidence_description,
            )
        except ConditionalCheckFailedException:
            LOGGER.error(
                "Cloud not upload evidence for finding %s", finding.id
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
    organization: str,
    finding: Optional[Finding] = None,
) -> None:
    machine_vulnerabilities = [
        vuln
        for vuln in sarif_log["runs"][0]["results"]
        if vuln["ruleId"] == vulnerability_id
    ]
    if finding is None:
        finding = await _create_draft(
            group_name,
            vulnerability_id,
            language,
            criteria_vulnerability,
            criteria_requirements,
        )
    try:
        integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
            vuln
            for vuln in await loaders.finding_vulnerabilities.load(finding.id)
            if vuln.state.status == VulnerabilityStateStatus.OPEN
            and vuln.state.source == Source.MACHINE
            and vuln.root_id == git_root.id
        )
    except FindingNotFound:
        return

    vulns_to_close = _build_vulnerabilities_stream_from_integrates(
        _machine_vulns_to_close(
            machine_vulnerabilities,
            integrates_vulnerabilities,
            execution_config,
        ),
        state="closed",
    )
    vulns_to_open = _build_vulnerabilities_stream_from_sarif(
        machine_vulnerabilities,
        sarif_log["runs"][0]["versionControlProvenance"][0]["revisionId"],
        git_root.state.nickname,
    )

    reattack_future = add_reattack_justification(
        finding.id,
        _get_vulns_with_reattack(
            vulns_to_open, integrates_vulnerabilities, "open"
        ),
        _get_vulns_with_reattack(
            vulns_to_open, integrates_vulnerabilities, "closed"
        ),
        sarif_log["runs"][0]["versionControlProvenance"][0]["revisionId"],
    )
    vulns_to_open = _filter_vulns_to_open(
        vulns_to_open, integrates_vulnerabilities
    )

    if await persist_vulnerabilities(
        loaders,
        group_name,
        git_root,
        finding,
        {
            "inputs": [*vulns_to_open["inputs"], *vulns_to_close["inputs"]],
            "lines": [*vulns_to_open["lines"], *vulns_to_close["lines"]],
        },
        organization,
    ):
        await reattack_future
        await upload_evidences(loaders, finding, machine_vulnerabilities)
    else:
        reattack_future.close()


async def process_execution(
    loaders: Dataloaders,
    execution_id: str,
    criteria_vulns: dict[str, Any],
    criteria_reqs: dict[str, Any],
) -> bool:
    boto3_session = aioboto3.Session()
    group_name = execution_id.split("_", maxsplit=1)[0]
    execution_config = await get_config(boto3_session, execution_id)
    try:
        git_root = next(  # noqa  # pylint: disabled=unused-variable
            root
            for root in await loaders.group_roots.load(group_name)
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
            and root.state.nickname == execution_config["namespace"]
        )
    except StopIteration:
        LOGGER.warning(
            "Cloud not find root %s for the execution %s",
            execution_config["namespace"],
            execution_id,
        )
        return False
    results = await get_sarif_log(boto3_session, execution_id)
    if not results:
        LOGGER.warning("Cloud not find execution result %s", execution_id)
        return False

    rules_id: Set[str] = {
        item["id"] for item in results["runs"][0]["tool"]["driver"]["rules"]
    }
    if not rules_id:
        return True

    group_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    rules_finding: Tuple[Tuple[str, Optional[Finding]], ...] = ()
    for criteria_vuln_id in rules_id:
        for finding in group_findings:
            if finding.title.startswith(f"{criteria_vuln_id}."):
                rules_finding = (*rules_finding, (criteria_vuln_id, finding))
                break
        else:
            rules_finding = (*rules_finding, (criteria_vuln_id, None))

    organization_name = (
        await loaders.organization.load(
            (await loaders.group.load(group_name)).organization_id
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
                organization=organization_name,
            )
            for vuln_id, finding in rules_finding
        ]
    )
    return True


def _decode_sqs_message(message: Any) -> str:
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
            LOGGER.error("An error ocurred in %s", message_id)
            LOGGER.error(str(exception))
        else:
            _delete_message(queue, message)


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    criteria_vulns = await get_vulns_file()
    criteria_reqs = get_requirements_file()
    sqs = boto3.resource("sqs", region_name=FI_AWS_REGION_NAME)
    queue = sqs.get_queue_by_name(QueueName="skims-report-queue")
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        while len(asyncio.all_tasks()) > 60:
            await asyncio.sleep(0.3)

        messages = queue.receive_messages(
            MessageAttributeNames=[],
            MaxNumberOfMessages=10,
            VisibilityTimeout=30,
        )
        for message in messages:
            task = asyncio.create_task(
                process_execution(
                    loaders,
                    _decode_sqs_message(message),
                    criteria_vulns,
                    criteria_reqs,
                )
            )
            task.add_done_callback(
                partial(_callback_done, message=message, queue=queue)
            )
