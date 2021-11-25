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
from custom_exceptions import (
    VulnNotFound,
    VulnNotInFinding,
)
from custom_types import (
    Finding as FindingType,
    Historic as HistoricType,
    User as UserType,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.vulnerabilities import (
    enums as vulns_enums,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from dynamodb.operations_legacy import (
    start_context,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
)
from itertools import (
    chain,
    zip_longest,
)
import logging
import logging.config
from mailer import (
    vulnerabilities as vulns_mail,
)
from newutils import (
    datetime as datetime_utils,
    requests as requests_utils,
    token as token_utils,
    vulnerabilities as vulns_utils,
)
from notifications import (
    domain as notifications_domain,
)
from operator import (
    attrgetter,
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
    Counter,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
)
import uuid
from vulnerabilities import (
    dal as vulns_dal,
)
from vulnerabilities.types import (
    FindingGroupedVulnerabilitiesInfo,
    GroupedVulnerabilitiesInfo,
    Treatments,
)
import yaml  # type: ignore

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def confirm_vulnerabilities_zero_risk(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    user_info: UserType,
    justification: str,
) -> bool:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_vuln_ids_new(
        loaders, finding_id, vuln_ids
    )
    vulnerabilities = tuple(
        vulns_utils.validate_zero_risk_requested(vuln)
        for vuln in vulnerabilities
    )
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
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
    await collect(
        vulns_dal.update_zero_risk(
            current_value=vuln.zero_risk,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            zero_risk=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                status=VulnerabilityZeroRiskStatus.CONFIRMED,
            ),
        )
        for vuln in vulnerabilities
    )
    if not add_comment[1]:
        LOGGER.error("An error occurred confirming zero risk vuln", **NOEXTRA)
        return False
    return True


async def _remove_all_tags(
    vulnerability: Vulnerability,
) -> None:
    await vulns_dal.update_metadata(
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        metadata=VulnerabilityMetadataToUpdate(
            tags=[],
        ),
    )


async def _remove_tag(
    vulnerability: Vulnerability,
    tag_to_remove: str,
) -> None:
    tags: Optional[List[str]] = vulnerability.tags
    if tags and tag_to_remove in tags:
        tags.remove(tag_to_remove)
        await vulns_dal.update_metadata(
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            metadata=VulnerabilityMetadataToUpdate(
                tags=tags,
            ),
        )


async def remove_vulnerability_tags(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    tag_to_remove: str,
) -> None:
    vulnerabilities = await get_by_finding_and_vuln_ids_new(
        loaders, finding_id, vuln_ids
    )
    if tag_to_remove:
        await collect(
            _remove_tag(vuln, tag_to_remove) for vuln in vulnerabilities
        )
        return
    await collect(_remove_all_tags(vuln) for vuln in vulnerabilities)


async def remove_vulnerability(  # pylint: disable=too-many-arguments
    loaders: Any,
    finding_id: str,
    vulnerability_id: str,
    justification: StateRemovalJustification,
    user_email: str,
    source: Source,
    include_closed_vuln: bool = False,
) -> bool:
    vulnerability: Vulnerability = await loaders.vulnerability_typed.load(
        vulnerability_id
    )
    if (
        vulnerability.state.status == VulnerabilityStateStatus.OPEN
        or include_closed_vuln
    ):
        await vulns_dal.update_state(
            finding_id=finding_id,
            vulnerability_id=vulnerability_id,
            state=VulnerabilityState(
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                source=source,
                status=VulnerabilityStateStatus.DELETED,
                justification=justification,
            ),
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


async def get_by_finding_and_vuln_ids_new(
    loaders: Any,
    finding_id: str,
    vuln_ids: Set[str],
) -> Tuple[Vulnerability, ...]:
    finding_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_typed.load(finding_id)
    filtered_vulns = tuple(
        vuln for vuln in finding_vulns if vuln.id in vuln_ids
    )
    if len(filtered_vulns) != len(vuln_ids):
        raise VulnNotInFinding()
    return filtered_vulns


async def get_by_vulnerabilities_ids(
    vulnerabilities_ids: List[str],
) -> Tuple[Dict[str, FindingType], ...]:
    vulnerabilities: Tuple[Dict[str, FindingType], ...] = tuple()
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(vulns_dal.TABLE_NAME)
        vulnerabilities = tuple(
            chain.from_iterable(
                await collect(
                    tuple(
                        vulns_dal.get_vulnerability_by_id(
                            vulnerability_id, table
                        )
                        for vulnerability_id in vulnerabilities_ids
                    )
                )
            )
        )

    if len(vulnerabilities) != len(vulnerabilities_ids):
        raise VulnNotFound()

    return vulnerabilities


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


async def get_open_vulnerabilities_specific_by_type(
    loaders: Any,
    finding_id: str,
) -> Dict[str, Tuple[Dict[str, str], ...]]:
    finding_vulns_loader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns_new(vulns)
    ports_vulns = tuple(
        {
            "where": vuln.where,
            "specific": vuln.specific,
            "commit_hash": "",
        }
        for vuln in open_vulns
        if vuln.type == vulns_enums.VulnerabilityType.PORTS
    )
    lines_vulns = tuple(
        {
            "where": vuln.where,
            "specific": vuln.specific,
            "commit_hash": vuln.commit if vuln.commit else "",
        }
        for vuln in open_vulns
        if vuln.type == vulns_enums.VulnerabilityType.LINES
    )
    inputs_vulns = tuple(
        {
            "where": vuln.where,
            "specific": vuln.specific,
            "commit_hash": "",
        }
        for vuln in open_vulns
        if vuln.type == vulns_enums.VulnerabilityType.INPUTS
    )
    return {
        "ports_vulnerabilities": ports_vulns,
        "lines_vulnerabilities": lines_vulns,
        "inputs_vulnerabilities": inputs_vulns,
    }


def get_treatments_count(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Treatments:
    treatment_counter = Counter(
        vuln.treatment.status
        for vuln in vulnerabilities
        if vuln.treatment
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    return Treatments(
        accepted=treatment_counter[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment_counter[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        in_progress=treatment_counter[
            VulnerabilityTreatmentStatus.IN_PROGRESS
        ],
        new=treatment_counter[VulnerabilityTreatmentStatus.NEW],
    )


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


async def mask_vulnerability(
    *,
    loaders: Any,
    finding_id: str,
    vulnerability_id: str,
) -> bool:
    historic_treatment_loader = loaders.vulnerability_historic_treatment
    historic_treatment: Tuple[
        VulnerabilityTreatment, ...
    ] = await historic_treatment_loader.load(vulnerability_id)
    masked_treatment = tuple(
        treatment._replace(
            manager="Masked" if treatment.manager else None,
            justification="Masked" if treatment.justification else None,
        )
        for treatment in historic_treatment
    )
    await vulns_dal.update_historic_treatment(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        historic_treatment=masked_treatment,
    )
    await vulns_dal.update_metadata(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        metadata=VulnerabilityMetadataToUpdate(
            specific="Masked",
            where="Masked",
        ),
    )
    return True


async def reject_vulnerabilities_zero_risk(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    user_info: UserType,
    justification: str,
) -> bool:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_vuln_ids_new(
        loaders, finding_id, vuln_ids
    )
    vulnerabilities = tuple(
        vulns_utils.validate_zero_risk_requested(vuln)
        for vuln in vulnerabilities
    )
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
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
    await collect(
        vulns_dal.update_zero_risk(
            current_value=vuln.zero_risk,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            zero_risk=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                status=VulnerabilityZeroRiskStatus.REJECTED,
            ),
        )
        for vuln in vulnerabilities
    )
    if not add_comment[1]:
        LOGGER.error("An error occurred rejecting zero risk vuln", **NOEXTRA)
        return False
    return True


async def request_verification(vulnerability: Vulnerability) -> bool:
    await vulns_dal.update_verification(
        current_value=vulnerability.verification,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        verification=VulnerabilityVerification(
            comment_id="",
            modified_by="",
            modified_date=datetime_utils.get_iso_date(),
            status=VulnerabilityVerificationStatus.REQUESTED,
        ),
    )
    return True


async def request_vulnerabilities_zero_risk(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    user_info: UserType,
    justification: str,
) -> bool:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_vuln_ids_new(
        loaders, finding_id, vuln_ids
    )
    vulnerabilities = tuple(
        vulns_utils.validate_non_zero_risk_requested(vuln)
        for vuln in vulnerabilities
    )
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
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
    await collect(
        vulns_dal.update_zero_risk(
            current_value=vuln.zero_risk,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            zero_risk=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                status=VulnerabilityZeroRiskStatus.REQUESTED,
            ),
        )
        for vuln in vulnerabilities
    )
    if not add_comment[1]:
        LOGGER.error("An error occurred requesting zero risk vuln", **NOEXTRA)
        return False
    await notifications_domain.request_vulnerability_zero_risk(
        loaders=loaders,
        finding_id=finding_id,
        justification=justification,
        requester_email=user_email,
    )
    return True


def get_updated_manager_mail_content(
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
        mail_content = get_updated_manager_mail_content(
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


async def update_metadata(
    *,
    loaders: Any,
    vulnerability_id: str,
    finding_id: str,
    bug_tracking_system_url: Optional[str],
    custom_severity: Optional[int],
    tags_to_append: Optional[List[str]],
) -> None:
    vulnerability: Vulnerability = await loaders.vulnerability_typed.load(
        vulnerability_id
    )
    all_tags = []
    if vulnerability.tags:
        all_tags.extend(vulnerability.tags)
    if tags_to_append:
        all_tags.extend(tags_to_append)
    await vulns_dal.update_metadata(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        metadata=VulnerabilityMetadataToUpdate(
            bug_tracking_system_url=bug_tracking_system_url,
            custom_severity=custom_severity,
            tags=sorted(list(set(all_tags))),
        ),
    )


async def update_metadata_and_state(
    *,
    vulnerability: Vulnerability,
    new_metadata: VulnerabilityMetadataToUpdate,
    new_state: VulnerabilityState,
    finding_policy: Optional[OrgFindingPolicyItem] = None,
) -> bool:
    """Update vulnerability metadata and historics."""
    if (
        vulnerability.state.source != new_state.source
        or vulnerability.state.status != new_state.status
    ):
        await vulns_dal.update_state(
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            state=new_state,
        )
        if (
            finding_policy
            and new_state.status == VulnerabilityStateStatus.OPEN
            and finding_policy.state.status == "APPROVED"
            and vulnerability.treatment.status
            != VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ):
            treatment_to_update = (
                vulns_utils.get_treatment_from_org_finding_policy_new(
                    modified_date=new_state.modified_date,
                    user_email=finding_policy.state.modified_by,
                )
            )
            await vulns_dal.update_treatment(
                current_value=vulnerability.treatment,
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                treatment=treatment_to_update[0],
            )
            await vulns_dal.update_treatment(
                current_value=treatment_to_update[0],
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                treatment=treatment_to_update[1],
            )

    await vulns_dal.update_metadata(
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        metadata=new_metadata,
    )
    return True


async def verify(
    *,
    context: Any,
    vulnerabilities: List[Vulnerability],
    modified_date: str,
    closed_vulns_ids: List[str],
    vulns_to_close_from_file: List[Vulnerability],
) -> bool:
    list_closed_vulns: List[Vulnerability] = sorted(
        [
            [vuln for vuln in vulnerabilities if vuln.id == closed_vuln][0]
            for closed_vuln in closed_vulns_ids
        ],
        key=attrgetter("id"),
    )
    source: Source = requests_utils.get_source_new(context)
    user_data: UserType = await token_utils.get_jwt_content(context)
    modified_by = str(user_data["user_email"])
    return all(
        await collect(
            update_metadata_and_state(
                vulnerability=vuln_to_close,
                new_metadata=VulnerabilityMetadataToUpdate(
                    commit=(
                        close_item.commit
                        if close_item
                        and close_item.type == VulnerabilityType.LINES
                        else None
                    ),
                    stream=(
                        close_item.stream
                        if close_item
                        and close_item.type == VulnerabilityType.INPUTS
                        else None
                    ),
                ),
                new_state=VulnerabilityState(
                    modified_by=modified_by,
                    modified_date=modified_date,
                    source=source,
                    status=VulnerabilityStateStatus.CLOSED,
                ),
            )
            for vuln_to_close, close_item in zip_longest(
                list_closed_vulns, vulns_to_close_from_file, fillvalue={}
            )
        )
    )


async def verify_vulnerability(vulnerability: Vulnerability) -> bool:
    await vulns_dal.update_verification(
        current_value=vulnerability.verification,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        verification=VulnerabilityVerification(
            comment_id="",
            modified_by="",
            modified_date=datetime_utils.get_iso_date(),
            status=VulnerabilityVerificationStatus.VERIFIED,
        ),
    )
    return True


async def close_by_exclusion(
    vulnerability: Vulnerability,
    modified_by: str,
    source: Source,
) -> None:
    if vulnerability.state.status not in {
        VulnerabilityStateStatus.CLOSED,
        VulnerabilityStateStatus.DELETED,
    }:
        await vulns_dal.update_state(
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            state=VulnerabilityState(
                modified_by=modified_by,
                modified_date=datetime_utils.get_iso_date(),
                source=source,
                status=VulnerabilityStateStatus.CLOSED,
                justification=StateRemovalJustification.EXCLUSION,
            ),
        )
        if vulns_utils.is_reattack_requested_new(vulnerability):
            await verify_vulnerability(vulnerability)
