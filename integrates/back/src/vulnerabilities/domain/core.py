# pylint:disable=too-many-lines

import aioboto3
from aioextensions import (
    collect,
    schedule,
)
from comments import (
    domain as comments_domain,
)
from contextlib import (
    AsyncExitStack,
)
import copy
from custom_exceptions import (
    VulnNotFound,
    VulnNotInFinding,
)
from custom_types import (
    Finding as FindingType,
    Historic as HistoricType,
    User as UserType,
    Vulnerability as VulnerabilityType,
)
from db_model.enums import (
    StateRemovalJustification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from dynamodb.operations_legacy import (
    start_context,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import html
import html.parser
from itertools import (
    zip_longest,
)
import logging
import logging.config
from mailer import (
    vulnerabilities as vulns_mail,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    requests as requests_utils,
    token as token_utils,
    utils,
    validations,
    vulnerabilities as vulns_utils,
)
from notifications import (
    domain as notifications_domain,
)
from operator import (
    itemgetter,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from starlette.datastructures import (
    UploadFile,
)
from time import (
    time,
)
from typing import (
    Any,
    cast,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
import uuid
from vulnerabilities import (
    dal as vulns_dal,
)
from vulnerabilities.types import (
    FindingGroupedVulnerabilitiesInfo,
    GroupedVulnerabilitiesInfo,
)
import yaml  # type: ignore

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _confirm_zero_risk(
    user_email: str,
    date: str,
    comment_id: str,
    vuln: VulnerabilityType,
) -> bool:
    historic_zero_risk: HistoricType = vuln.get("historic_zero_risk", [])
    new_state = {
        "comment_id": comment_id,
        "date": date,
        "email": user_email,
        "status": "CONFIRMED",
    }
    historic_zero_risk.append(new_state)
    return await vulns_dal.update(
        vuln["finding_id"],
        vuln["UUID"],
        {"historic_zero_risk": historic_zero_risk},
    )


async def confirm_vulnerabilities_zero_risk(
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str],
) -> bool:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        vulns_utils.validate_requested_vuln_zero_risk(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info["user_email"]
    comment_data = {
        "comment_type": "zero_risk",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    add_comment = await comments_domain.add(
        finding_id, comment_data, user_info
    )
    confirm_zero_risk_vulns = await collect(
        [
            _confirm_zero_risk(user_email, today, comment_id, vuln)
            for vuln in vulnerabilities
        ]
    )
    success = all(confirm_zero_risk_vulns) and add_comment[1]
    if not success:
        LOGGER.error("An error occurred confirming zero risk vuln", **NOEXTRA)
    return success


async def remove_vulnerability_tags(
    finding_id: str, vulnerabilities: List[str], tag: str
) -> bool:
    vuln_update_coroutines = []
    vuln_info = await get_by_finding_and_uuids(
        finding_id, set(vulnerabilities)
    )
    for index, vulnerability in enumerate(vulnerabilities):
        tag_info: Dict[str, Optional[Set[str]]] = {"tag": set()}
        if tag:
            if vuln_info[index]:
                tag_info["tag"] = cast(
                    Set[str], vuln_info[index].get("tag", [])
                )
            if tag in cast(Set[str], tag_info.get("tag", [])):
                cast(Set[str], tag_info.get("tag")).remove(tag)
        if tag_info.get("tag") == set():
            tag_info["tag"] = None
        vuln_update_coroutines.append(
            vulns_dal.update(
                finding_id,
                vulnerability,
                cast(Dict[str, FindingType], tag_info),
            )
        )
    success = await collect(vuln_update_coroutines)
    return all(success)


async def remove_vulnerability(  # pylint: disable=too-many-arguments
    loaders: Any,
    finding_id: str,
    vulnerability_id: str,
    justification: StateRemovalJustification,
    user_email: str,
    source: str,
    include_closed_vuln: bool = False,
) -> bool:
    vulnerability: Vulnerability = await loaders.vulnerability_typed.load(
        vulnerability_id
    )
    if (
        vulnerability.state.status == VulnerabilityStateStatus.OPEN
        or include_closed_vuln
    ):
        await vulns_dal.append(
            finding_id=finding_id,
            vulnerability_id=vulnerability_id,
            elements={
                "historic_state": (
                    {
                        "analyst": user_email,
                        "date": datetime_utils.get_now_as_str(),
                        "justification": justification.value,
                        "source": source,
                        "state": "DELETED",
                    },
                )
            },
        )
        return True
    return False


async def get(vuln_id: str) -> Dict[str, FindingType]:
    vuln = await vulns_dal.get(vuln_id)
    if not vuln:
        raise VulnNotFound()
    first_vuln = cast(Dict[str, List[Dict[str, str]]], vuln[0])
    if (
        first_vuln.get("historic_state", [{}])[-1].get("state", "")
        == "DELETED"
    ):
        raise VulnNotFound()
    return vuln[0]


async def get_by_finding(
    finding_id: str, vuln_id: str
) -> Dict[str, FindingType]:
    vuln = await vulns_dal.get_by_finding(finding_id, uuid=vuln_id)
    first_vuln = cast(Dict[str, List[Dict[str, str]]], vuln[0])
    if not vuln:
        raise VulnNotFound()
    if (
        first_vuln.get("historic_state", [{}])[-1].get("state", "")
        == "DELETED"
    ):
        raise VulnNotFound()
    return vuln[0]


async def get_by_finding_and_uuids(
    finding_id: str,
    vuln_ids: Set[str],
) -> List[Dict[str, FindingType]]:
    finding_vulns = await vulns_dal.get_by_finding(finding_id)
    fin_vulns = [vuln for vuln in finding_vulns if vuln["UUID"] in vuln_ids]
    if len(fin_vulns) != len(vuln_ids):
        raise VulnNotInFinding()

    vulns = vulns_utils.filter_non_deleted(fin_vulns)
    if len(vulns) != len(vuln_ids):
        raise VulnNotFound()
    return vulns


async def get_by_ids(vulns_ids: List[str]) -> List[Dict[str, FindingType]]:
    result: List[Dict[str, FindingType]] = await collect(
        [get(vuln_id) for vuln_id in vulns_ids]
    )
    return result


async def get_grouped_vulnerabilities_info(
    loaders: Any,
    finding_id: str,
) -> FindingGroupedVulnerabilitiesInfo:
    vulnerabilities_by_type = await get_open_vulnerabilities_specific_by_type(
        loaders, finding_id
    )
    ports_vulnerabilities = vulnerabilities_by_type["ports_vulnerabilities"]
    lines_vulnerabilities = vulnerabilities_by_type["lines_vulnerabilities"]
    inputs_vulnerabilities = vulnerabilities_by_type["inputs_vulnerabilities"]
    grouped_ports_vulnerabilities: Tuple[
        GroupedVulnerabilitiesInfo, ...
    ] = tuple()
    grouped_inputs_vulnerabilities: Tuple[
        GroupedVulnerabilitiesInfo, ...
    ] = tuple()
    grouped_lines_vulnerabilities: Tuple[
        GroupedVulnerabilitiesInfo, ...
    ] = tuple()
    where = "-"
    if ports_vulnerabilities:
        grouped_ports_vulnerabilities = tuple(
            map(
                lambda grouped_vulns_info: GroupedVulnerabilitiesInfo(
                    where=grouped_vulns_info["where"],
                    specific=grouped_vulns_info["specific"],
                    commit_hash=grouped_vulns_info.get("commit_hash"),
                ),
                vulns_utils.group_specific(ports_vulnerabilities, "ports"),
            )
        )
        where = vulns_utils.format_where(where, ports_vulnerabilities)

    if lines_vulnerabilities:
        grouped_lines_vulnerabilities = tuple(
            map(
                lambda grouped_vulns_info: GroupedVulnerabilitiesInfo(
                    where=grouped_vulns_info["where"],
                    specific=grouped_vulns_info["specific"],
                    commit_hash=grouped_vulns_info.get("commit_hash"),
                ),
                vulns_utils.group_specific(lines_vulnerabilities, "lines"),
            )
        )
        where = vulns_utils.format_where(where, lines_vulnerabilities)

    if inputs_vulnerabilities:
        grouped_inputs_vulnerabilities = tuple(
            map(
                lambda grouped_vulns_info: GroupedVulnerabilitiesInfo(
                    where=grouped_vulns_info["where"],
                    specific=grouped_vulns_info["specific"],
                    commit_hash=grouped_vulns_info.get("commit_hash"),
                ),
                vulns_utils.group_specific(inputs_vulnerabilities, "inputs"),
            )
        )
        where = vulns_utils.format_where(where, inputs_vulnerabilities)

    grouped_vulnerabilities_info = FindingGroupedVulnerabilitiesInfo(
        where=where,
        grouped_ports_vulnerabilities=grouped_ports_vulnerabilities,
        grouped_lines_vulnerabilities=grouped_lines_vulnerabilities,
        grouped_inputs_vulnerabilities=grouped_inputs_vulnerabilities,
    )
    return grouped_vulnerabilities_info


async def get_open_vuln_by_type(
    context: Any,
    finding_id: str,
) -> Dict[str, Union[int, List[Dict[str, str]]]]:
    """Get open vulnerabilities group by type."""
    finding_vulns_loader = context.finding_vulns_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    finding: Dict[str, Union[int, List[Dict[str, str]]]] = {
        "openVulnerabilities": 0,
        "closedVulnerabilities": 0,
        "portsVulns": [],
        "linesVulns": [],
        "inputsVulns": [],
    }
    vulns_types = ["ports", "lines", "inputs"]
    for vuln in vulnerabilities:
        current_state = vulns_utils.get_last_status(vuln)
        if current_state == "open":
            finding["openVulnerabilities"] = (
                cast(int, finding["openVulnerabilities"]) + 1
            )
            if vuln.get("vuln_type") in vulns_types:
                cast(
                    List[Dict[str, str]],
                    finding[f'{vuln.get("vuln_type", "")}Vulns'],
                ).append(
                    {
                        "where": vuln.get("where"),
                        "specific": vuln.get("specific"),
                        "commit_hash": vuln.get("commit_hash"),
                    }
                )
            else:
                LOGGER.error(
                    "Vulnerability does not have the right type",
                    extra={
                        "extra": {
                            "vuln_uuid": vuln.get("UUID"),
                            "finding_id": finding_id,
                        }
                    },
                )
        elif current_state == "closed":
            finding["closedVulnerabilities"] = (
                cast(int, finding["closedVulnerabilities"]) + 1
            )
        else:
            LOGGER.error(
                "Error: Vulnerability does not have the right state",
                extra={
                    "extra": {
                        "vuln_uuid": vuln["UUID"],
                        "finding_id": finding_id,
                    }
                },
            )
    return finding


async def get_open_vulnerabilities_specific_by_type(
    loaders: Any,
    finding_id: str,
) -> Dict[str, Tuple[Dict[str, str], ...]]:
    finding_vulns_loader = loaders.finding_vulns_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    ports_vulnerabilities = []
    lines_vulnerabilities = []
    inputs_vulnerabilities = []
    vulns_types = ["ports", "lines", "inputs"]
    for vulnerability in vulnerabilities:
        current_state = vulns_utils.get_last_status(vulnerability)
        if current_state == "open":
            vulnerability_info: Dict[str, str] = {
                "where": vulnerability.get("where", ""),
                "specific": vulnerability.get("specific", ""),
                "commit_hash": vulnerability.get("commit_hash", ""),
            }
            if vulnerability.get("vuln_type") in vulns_types:
                if vulnerability["vuln_type"] == "ports":
                    ports_vulnerabilities.append(vulnerability_info)
                if vulnerability["vuln_type"] == "lines":
                    lines_vulnerabilities.append(vulnerability_info)
                if vulnerability["vuln_type"] == "inputs":
                    inputs_vulnerabilities.append(vulnerability_info)
            else:
                LOGGER.error(
                    "Vulnerability does not have the right type",
                    extra={
                        "extra": {
                            "vuln_uuid": vulnerability["UUID"],
                            "finding_id": finding_id,
                        }
                    },
                )
        elif current_state == "closed":
            pass
        else:
            LOGGER.error(
                "Error: Vulnerability does not have the right state",
                extra={
                    "extra": {
                        "vuln_uuid": vulnerability["UUID"],
                        "finding_id": finding_id,
                    }
                },
            )

    return {
        "ports_vulnerabilities": tuple(ports_vulnerabilities),
        "lines_vulnerabilities": tuple(lines_vulnerabilities),
        "inputs_vulnerabilities": tuple(inputs_vulnerabilities),
    }


async def get_vulnerabilities_async(
    finding_id: str,
    table: aioboto3.session.Session.client,
    should_list_deleted: bool = False,
) -> List[Dict[str, FindingType]]:
    vulnerabilities = await vulns_dal.get_vulnerabilities_async(
        finding_id, table, should_list_deleted
    )
    return [vulns_utils.format_data(vuln) for vuln in vulnerabilities]


async def get_vulnerabilities_by_type(
    context: Any, finding_id: str
) -> Dict[str, List[FindingType]]:
    """Get vulnerabilities group by type."""
    finding_vulns_loader = context.finding_vulns_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    vulnerabilities_formatted = vulns_utils.format_vulnerabilities(
        vulnerabilities
    )
    return vulnerabilities_formatted


async def get_vulnerabilities_file(
    context: Any, finding_id: str, group_name: str
) -> str:
    vulnerabilities = await get_vulnerabilities_by_type(context, finding_id)
    # FP: the generated filename is unpredictable
    file_name = f"/tmp/{group_name}-{finding_id}_{str(uuid.uuid4())}.yaml"  # NOSONAR # nosec # noqa: E501
    with open(  # pylint: disable=unspecified-encoding
        file_name, "w"
    ) as stream:
        yaml.safe_dump(vulnerabilities, stream, default_flow_style=False)

    uploaded_file_url = ""
    with open(file_name, "rb") as bstream:
        uploaded_file = UploadFile(
            filename=bstream.name, content_type="application/yaml"
        )
        await uploaded_file.write(bstream.read())
        await uploaded_file.seek(0)
        uploaded_file_name = await vulns_dal.upload_file(uploaded_file)
        uploaded_file_url = await vulns_dal.sign_url(uploaded_file_name)
    return uploaded_file_url


def group_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[FindingType]:
    """Group vulnerabilities by specific field."""
    vuln_types = ["lines", "ports", "inputs"]
    vuln_states = ["open", "closed"]
    total_vulnerabilities: Dict[str, Dict[str, FindingType]] = {}
    result_vulns: List[FindingType] = []
    for vuln_type in vuln_types:
        total_vulnerabilities[vuln_type] = {}
        for vuln_state in vuln_states:
            total_vulnerabilities[vuln_type][vuln_state] = []

    for vuln in vulnerabilities:
        all_states = cast(
            List[Dict[str, FindingType]], vuln.get("historic_state", [{}])
        )
        current_state = str(all_states[-1].get("state", ""))
        vuln_type = str(vuln.get("vuln_type", ""))
        cast(
            List[Dict[str, FindingType]],
            total_vulnerabilities[vuln_type][current_state],
        ).append(vuln)

    for vuln_type in vuln_types:
        for vuln_state in vuln_states:
            vulns_grouped = cast(
                Iterable[FindingType],
                vulns_utils.group_specific(
                    cast(
                        List[str], total_vulnerabilities[vuln_type][vuln_state]
                    ),
                    vuln_type,
                ),
            )
            result_vulns.extend(vulns_grouped)
    return result_vulns


async def list_vulnerabilities_async(
    finding_ids: List[str],
    should_list_deleted: bool = False,
    include_requested_zero_risk: bool = False,
    include_confirmed_zero_risk: bool = False,
) -> List[Dict[str, FindingType]]:
    """Retrieves all vulnerabilities for the requested findings"""
    vulns: List[Dict[str, FindingType]] = []
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(vulns_dal.TABLE_NAME)
        vulns = await collect(
            [
                get_vulnerabilities_async(
                    finding_id, table, should_list_deleted
                )
                for finding_id in finding_ids
            ]
        )

    result: List[Dict[str, FindingType]] = []
    for result_list in vulns:
        result.extend(cast(Iterable[Dict[str, FindingType]], result_list))
    if not include_requested_zero_risk:
        result = vulns_utils.filter_non_requested_zero_risk(result)
    if not include_confirmed_zero_risk:
        result = vulns_utils.filter_non_confirmed_zero_risk(result)
    return result


async def mask_vuln(vuln: Vulnerability) -> bool:
    items: List[VulnerabilityType] = await vulns_dal.get(vuln.id)
    item: VulnerabilityType = items[0]
    historic_treatment: Optional[HistoricType] = item.get("historic_treatment")
    if historic_treatment:
        for state in historic_treatment:
            if "treatment_manager" in state:
                state["treatment_manager"] = "Masked"
            if "justification" in state:
                state["justification"] = "Masked"
    return await vulns_dal.update(
        vuln.finding_id,
        vuln.id,
        {
            "specific": "Masked",
            "where": "Masked",
            "historic_treatment": historic_treatment,
        },
    )


async def _reject_zero_risk(
    user_email: str,
    date: str,
    comment_id: str,
    vuln: VulnerabilityType,
) -> bool:
    historic_zero_risk: HistoricType = vuln.get("historic_zero_risk", [])
    new_state = {
        "comment_id": comment_id,
        "date": date,
        "email": user_email,
        "status": "REJECTED",
    }
    historic_zero_risk.append(new_state)
    return await vulns_dal.update(
        vuln["finding_id"],
        vuln["UUID"],
        {"historic_zero_risk": historic_zero_risk},
    )


async def reject_vulnerabilities_zero_risk(
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str],
) -> bool:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        vulns_utils.validate_requested_vuln_zero_risk(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info["user_email"]
    comment_data = {
        "comment_type": "zero_risk",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    add_comment = await comments_domain.add(
        finding_id, comment_data, user_info
    )
    reject_zero_risk_vulns = await collect(
        [
            _reject_zero_risk(user_email, today, str(comment_id), vuln)
            for vuln in vulnerabilities
        ]
    )
    success = all(reject_zero_risk_vulns) and add_comment[1]
    if not success:
        LOGGER.error("An error occurred rejecting zero risk vuln", **NOEXTRA)
    return success


async def request_verification(vuln: VulnerabilityType) -> bool:
    today = datetime_utils.get_now_as_str()
    historic_verification: HistoricType = vuln.get("historic_verification", [])
    new_state = {
        "date": today,
        "status": "REQUESTED",
    }
    historic_verification.append(new_state)
    return await vulns_dal.update(
        vuln["finding_id"],
        vuln["UUID"],
        {"historic_verification": historic_verification},
    )


async def _request_zero_risk(
    user_email: str,
    date: str,
    comment_id: str,
    vuln: VulnerabilityType,
) -> bool:
    historic_zero_risk: HistoricType = vuln.get("historic_zero_risk", [])
    new_state = {
        "comment_id": comment_id,
        "date": date,
        "email": user_email,
        "status": "REQUESTED",
    }
    historic_zero_risk.append(new_state)
    return await vulns_dal.update(
        vuln["finding_id"],
        vuln["UUID"],
        {"historic_zero_risk": historic_zero_risk},
    )


async def request_vulnerabilities_zero_risk(
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vuln_ids: List[str],
) -> bool:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_uuids(finding_id, set(vuln_ids))
    vulnerabilities = [
        vulns_utils.validate_not_requested_zero_risk_vuln(vuln)
        for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    comment_data = {
        "comment_type": "zero_risk",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    add_comment = await comments_domain.add(
        finding_id, comment_data, user_info
    )
    request_zero_risk_vulns = await collect(
        [
            _request_zero_risk(user_email, today, str(comment_id), vuln)
            for vuln in vulnerabilities
        ]
    )
    success = all(request_zero_risk_vulns) and add_comment[1]
    if success:
        await notifications_domain.request_vulnerability_zero_risk(
            info=info,
            finding_id=finding_id,
            justification=justification,
            requester_email=user_email,
        )
    else:
        LOGGER.error("An error occurred requesting zero risk vuln", **NOEXTRA)
    return success


def set_updated_manager_mail_content(
    vulnerabilities: Dict[str, List[Dict[str, str]]]
) -> str:
    mail_content = ""
    for vuln_type in ["ports", "lines", "inputs"]:
        type_vulns = vulnerabilities.get(vuln_type)
        if type_vulns:
            mail_content += "\n".join(
                [
                    f"- {list(vuln.values())[0]} ({list(vuln.values())[1]})"
                    for vuln in type_vulns
                ]
            )
            mail_content += "\n"
    return mail_content


async def should_send_update_treatment(
    *,
    loaders: Any,
    finding_id: str,
    finding_title: str,
    group_name: str,
    treatment: str,
    updated_vulns: List[Dict[str, FindingType]],
) -> None:
    translations = {"IN PROGRESS": "In Progress"}
    if treatment in translations:
        vulns_grouped = group_vulnerabilities(updated_vulns)
        vulns_data = vulns_utils.format_vulnerabilities(
            cast(List[Dict[str, FindingType]], vulns_grouped)
        )
        mail_content = set_updated_manager_mail_content(
            cast(Dict[str, List[Dict[str, str]]], vulns_data)
        )
        schedule(
            vulns_mail.send_mail_updated_treatment(
                loaders=loaders,
                finding_id=finding_id,
                finding_title=finding_title,
                group_name=group_name,
                treatment=translations[treatment],
                vulnerabilities=mail_content,
            )
        )


async def update_historics_dates(
    finding_id: str, vuln: Dict[str, FindingType], date: str
) -> bool:
    """Set historic dates to finding's discovery date"""
    historic_state = cast(HistoricType, vuln["historic_state"])
    for state_info in historic_state:
        state_info["date"] = date
    historic_treatment = cast(HistoricType, vuln["historic_treatment"])
    for treatment_info in historic_treatment:
        treatment_info["date"] = date
    success = await vulns_dal.update(
        finding_id,
        cast(str, vuln["UUID"]),
        {
            "historic_state": historic_state,
            "historic_treatment": historic_treatment,
        },
    )
    return success


async def update_treatment_vuln(
    vulnerability: Vulnerability,
    finding_id: str,
    updated_values: Dict[str, FindingType],
    info: GraphQLResolveInfo,
) -> bool:
    success = True
    new_info = copy.copy(updated_values)
    if new_info.get("tag"):
        new_info["tag"] = vulnerability.tags or []
        tags = str(updated_values["tag"]).split(",")
        validations.validate_fields(tags)
        for tag in tags:
            if tag.strip():
                validations.validate_field_length(tag.strip(), 30)
                cast(List[str], new_info["tag"]).append(tag.strip())
        new_info["tag"] = cast(
            List[str],
            list(set(cast(Iterable[Collection[str]], new_info["tag"]))),
        )
        new_info["tag"] = [
            html.unescape(tag) for tag in cast(List[str], new_info["tag"])
        ]
    new_info = {
        key: None if not value else value for key, value in new_info.items()
    }
    new_info = {
        utils.camelcase_to_snakecase(k): new_info.get(k) for k in new_info
    }
    result_update_vuln = await vulns_dal.update(
        finding_id, vulnerability.id, new_info
    )
    if not result_update_vuln:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update vulnerability: "
            f"{vulnerability.id} from finding:{finding_id}",
        )
        success = False
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated vulnerability: "
            f"{vulnerability.id} from finding: {finding_id} successfully",
        )
    return success


async def update_treatment_vulns(
    vulnerability_id: str,
    finding_id: str,
    updated_values: Dict[str, FindingType],
    info: GraphQLResolveInfo,
) -> bool:
    del updated_values["finding_id"]
    loaders = info.context.loaders
    vulnerability: Vulnerability = await loaders.vulnerability_typed.load(
        vulnerability_id
    )
    success: bool = await update_treatment_vuln(
        vulnerability, finding_id, updated_values, info
    )
    return success


async def update_treatments(
    vulnerability_id: str,
    finding_id: str,
    updated_values: Dict[str, FindingType],
    info: GraphQLResolveInfo,
) -> bool:
    updated_values.pop("vulnerabilities", None)
    if updated_values.get("tag") == "":
        updated_values.pop("tag", None)
    if cast(int, updated_values.get("severity", 0)) < 0:
        updated_values["severity"] = ""
    if "external_bts" in updated_values:
        validations.validate_url(str(updated_values.get("external_bts", "")))
        validations.validate_field_length(
            str(updated_values.get("external_bts", "")), 80
        )
    return await update_treatment_vulns(
        vulnerability_id, finding_id, updated_values, info
    )


async def update_vuln_state(
    *,
    info: GraphQLResolveInfo,
    vulnerability: Dict[str, FindingType],
    item: Dict[str, str],
    finding_id: str,
    current_day: str,
    finding_policy: Optional[OrgFindingPolicyItem] = None,
) -> bool:
    """Update vulnerability state."""
    historic_state = cast(
        List[Dict[str, str]], vulnerability.get("historic_state")
    )
    last_state = historic_state[-1]
    data_to_update: Dict[str, FindingType] = {}

    source = requests_utils.get_source(info.context)

    if last_state.get("source") != source or last_state.get(
        "state"
    ) != item.get("state"):
        user_data = cast(
            UserType, await token_utils.get_jwt_content(info.context)
        )
        analyst = str(user_data["user_email"])
        current_state = {
            "analyst": analyst,
            "date": current_day,
            "source": source,
            "state": item.get("state", ""),
        }
        historic_state.append(current_state)
        data_to_update["historic_state"] = historic_state
        curr_treatment = vulnerability["historic_treatment"][-1]["treatment"]
        if (
            finding_policy
            and item["state"] == "open"
            and finding_policy.state.status == "APPROVED"
            and curr_treatment != "ACCEPTED_UNDEFINED"
        ):
            data_to_update["historic_treatment"] = [
                *vulnerability["historic_treatment"],
                *vulns_utils.get_treatment_from_org_finding_policy(
                    current_day=current_day,
                    user_email=finding_policy.state.modified_by,
                ),
            ]

    if item["vuln_type"] == "inputs":
        data_to_update["stream"] = item["stream"]
    if item["vuln_type"] == "lines":
        data_to_update["commit_hash"] = item["commit_hash"]
    if "repo_nickname" in item:
        data_to_update["repo_nickname"] = item["repo_nickname"]

    if data_to_update:
        return await vulns_dal.update(
            finding_id, str(vulnerability.get("UUID")), data_to_update
        )
    return True


async def verify(
    *,
    info: GraphQLResolveInfo,
    finding_id: str,
    vulnerabilities: List[Dict[str, FindingType]],
    closed_vulnerabilities: List[str],
    date: str,
    vulns_to_close_from_file: List[Dict[str, str]],
) -> List[bool]:
    list_closed_vulns = sorted(
        [
            [vuln for vuln in vulnerabilities if vuln["UUID"] == closed_vuln][
                0
            ]
            for closed_vuln in closed_vulnerabilities
        ],
        key=itemgetter("UUID"),
    )
    success: List[bool] = await collect(
        update_vuln_state(
            info=info,
            vulnerability=vuln_to_close,
            item={
                "commit_hash": (
                    close_item["commit_hash"]
                    if close_item and close_item["vuln_type"] == "lines"
                    else ""
                ),
                "state": "closed",
                "stream": (
                    close_item["stream"]
                    if close_item and close_item["vuln_type"] == "inputs"
                    else ""
                ),
                "vuln_type": close_item["vuln_type"] if close_item else "",
            },
            finding_id=finding_id,
            current_day=date,
        )
        for vuln_to_close, close_item in zip_longest(
            list_closed_vulns, vulns_to_close_from_file, fillvalue={}
        )
    )
    return success


async def verify_vulnerability(vuln: VulnerabilityType) -> bool:
    today = datetime_utils.get_now_as_str()
    historic_verification: HistoricType = vuln.get("historic_verification", [])
    new_state = {
        "date": today,
        "status": "VERIFIED",
    }
    historic_verification.append(new_state)
    return await vulns_dal.update(
        vuln["finding_id"],
        vuln["UUID"],
        {"historic_verification": historic_verification},
    )


async def close_by_exclusion(vuln: Dict[str, Any]) -> None:
    current_state = vuln["historic_state"][-1]["state"]

    if current_state not in {"closed", "DELETED"}:
        await vulns_dal.update(
            vuln["finding_id"],
            vuln["UUID"],
            {
                "historic_state": [
                    *vuln["historic_state"],
                    {
                        **vuln["historic_state"][-1],
                        "state": "closed",
                        "justification": "EXCLUSION",
                    },
                ]
            },
        )
        if vulns_utils.is_reattack_requested(vuln):
            await verify_vulnerability(vuln)
