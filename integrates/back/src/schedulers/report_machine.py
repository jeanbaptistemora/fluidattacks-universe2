import aioboto3
from aioextensions import (
    collect,
)
from aiohttp.client_exceptions import (
    ClientPayloadError,
)
import base64
import boto3
from context import (
    FI_AWS_REGION_NAME,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidUrl,
    ToeInputNotFound,
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
from finding_comments import (
    domain as comments_domain,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDraftToAdd,
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
from organizations_finding_policies import (
    domain as policies_domain,
)
import pytz  # type: ignore
from settings.various import (
    TIME_ZONE,
)
from signal import (
    SIGINT,
    signal,
    SIGTERM,
)
import tempfile
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

LOGGER = logging.getLogger(__name__)


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
        with suppress(InvalidUrl, ToeInputNotFound):
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
        )
        return result
    LOGGER.warning(
        "No vulnerabilities found to modify for finding %s", finding.id
    )
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


async def process_criteria_vuln(
    loaders: Dataloaders,
    group_name: str,
    vulnerability_id: str,
    criteria_vulnerability: Dict[str, Any],
    criteria_requirements: Dict[str, Any],
    **kwargs: Any,
) -> None:
    finding: Optional[Finding] = kwargs.get("finding", None)
    git_root: GitRoot = kwargs["git_root"]
    sarif_log: Dict[str, Any] = kwargs["sarif_log"]
    machine_vulnerabilities = [
        vuln
        for vuln in sarif_log["runs"][0]["results"]
        if vuln["ruleId"] == vulnerability_id
    ]
    execution_config: Dict[str, Any] = kwargs["execution_config"]
    if finding is None:
        LOGGER.info("Cloud not find a finding for %s", vulnerability_id)
        finding = await _create_draft(
            group_name,
            vulnerability_id,
            kwargs["language"],
            criteria_vulnerability,
            criteria_requirements,
        )

    integrates_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
        vuln
        for vuln in await loaders.finding_vulnerabilities.load(finding.id)
        if vuln.state.status == VulnerabilityStateStatus.OPEN
        and vuln.state.source == Source.MACHINE
        and vuln.root_id == git_root.id
    )
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
        kwargs["organization"],
    ):
        await reattack_future


async def process_execution(
    loaders: Dataloaders,
    boto3_session: aioboto3.Session,
    execution_id: str,
    criteria_vulns: dict[str, Any],
    criteria_reqs: dict[str, Any],
) -> bool:
    LOGGER.info("Processing the execution %s", execution_id)
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

    rules_id: List[str] = [
        item["id"] for item in results["runs"][0]["tool"]["driver"]["rules"]
    ]
    if not rules_id:
        LOGGER.info("Execution %s has no results", execution_id)
    group_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    group_findings = tuple(
        finding
        for finding in group_findings
        if any(rule in finding.title for rule in rules_id)
    )
    rules_finding: Tuple[Tuple[str, Optional[Finding]], ...] = ()
    for vuln_id in rules_id:
        for finding in group_findings:
            if vuln_id in finding.title:
                rules_finding = (*rules_finding, (vuln_id, finding))
                break
        else:
            rules_finding = (*rules_finding, (vuln_id, None))

    organization_name = (
        await loaders.organization.load(
            (await loaders.group.load(group_name)).organization_id
        )
    ).name
    LOGGER.info(
        "Processing %s findings in the execution %s",
        len(rules_finding),
        execution_id,
    )
    await collect(
        [
            process_criteria_vuln(
                loaders,
                group_name,
                vuln_id,
                criteria_vulns[vuln_id],
                criteria_reqs,
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


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    criteria_vulns = await get_vulns_file()
    criteria_reqs = get_requirements_file()
    session = aioboto3.Session()
    sqs = boto3.resource("sqs", region_name=FI_AWS_REGION_NAME)
    queue = sqs.get_queue_by_name(QueueName="skims-report-queue")
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        messages = queue.receive_messages(
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=3,
        )
        futures = [
            process_execution(
                loaders,
                session,
                _decode_sqs_message(message),
                criteria_vulns,
                criteria_reqs,
            )
            for message in messages
        ]
        await collect(futures)
