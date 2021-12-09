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
    Counter,
    Dict,
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
    vulnerabilities = await get_by_finding_and_vuln_ids(
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


async def add_tags(
    vulnerability: Vulnerability,
    tags: List[str],
) -> None:
    if not tags:
        return
    if vulnerability.tags:
        tags.extend(vulnerability.tags)
    await vulns_dal.update_metadata(
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        metadata=VulnerabilityMetadataToUpdate(
            tags=sorted(list(set(tags))),
        ),
    )


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
    vulnerabilities = await get_by_finding_and_vuln_ids(
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


async def get_by_finding_and_vuln_ids(
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
                    ),
                    workers=1024,
                )
            )
        )

    if len(vulnerabilities) != len(vulnerabilities_ids):
        raise VulnNotFound()

    return vulnerabilities


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
                    where=grouped_vulns_info.where,
                    specific=grouped_vulns_info.specific,
                    commit_hash=grouped_vulns_info.commit
                    if grouped_vulns_info.commit is not None
                    else "",
                ),
                vulns_utils.group_specific(
                    ports_vulnerabilities, VulnerabilityType.PORTS
                ),
            )
        )
        where = vulns_utils.format_where(where, ports_vulnerabilities)

    if lines_vulnerabilities:
        grouped_lines_vulnerabilities = tuple(
            map(
                lambda grouped_vulns_info: GroupedVulnerabilitiesInfo(
                    where=grouped_vulns_info.where,
                    specific=grouped_vulns_info.specific,
                    commit_hash=grouped_vulns_info.commit
                    if grouped_vulns_info.commit is not None
                    else "",
                ),
                vulns_utils.group_specific(
                    lines_vulnerabilities, VulnerabilityType.LINES
                ),
            )
        )
        where = vulns_utils.format_where(where, lines_vulnerabilities)

    if inputs_vulnerabilities:
        grouped_inputs_vulnerabilities = tuple(
            map(
                lambda grouped_vulns_info: GroupedVulnerabilitiesInfo(
                    where=grouped_vulns_info.where,
                    specific=grouped_vulns_info.specific,
                    commit_hash=grouped_vulns_info.commit
                    if grouped_vulns_info.commit is not None
                    else "",
                ),
                vulns_utils.group_specific(
                    inputs_vulnerabilities, VulnerabilityType.INPUTS
                ),
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
) -> Dict[str, Tuple[Vulnerability, ...]]:
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_nzr_typed.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    ports_vulns = tuple(
        vuln
        for vuln in open_vulns
        if vuln.type == vulns_enums.VulnerabilityType.PORTS
    )
    lines_vulns = tuple(
        vuln
        for vuln in open_vulns
        if vuln.type == vulns_enums.VulnerabilityType.LINES
    )
    inputs_vulns = tuple(
        vuln
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


async def get_vulnerabilities_by_type(
    loaders: Any, finding_id: str
) -> Dict[str, List[Dict[str, str]]]:
    """Get vulnerabilities group by type."""
    vulnerabilities = await loaders.finding_vulns_nzr_typed.load(finding_id)
    vulnerabilities_formatted = vulns_utils.format_vulnerabilities(
        vulnerabilities
    )
    return vulnerabilities_formatted


async def get_vulnerabilities_file(
    loaders: Any, finding_id: str, group_name: str
) -> str:
    vulnerabilities = await get_vulnerabilities_by_type(loaders, finding_id)
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
    vulnerabilities: Tuple[Vulnerability, ...]
) -> Tuple[Vulnerability, ...]:
    """Group vulnerabilities by specific field."""
    vuln_types = (
        VulnerabilityType.LINES,
        VulnerabilityType.PORTS,
        VulnerabilityType.INPUTS,
    )
    vuln_states = (
        VulnerabilityStateStatus.OPEN,
        VulnerabilityStateStatus.CLOSED,
    )
    total_vulnerabilities: Dict[str, Dict[str, List[Vulnerability]]] = {}
    result_vulns = []
    for vuln_type in vuln_types:
        total_vulnerabilities[vuln_type] = {}
        for vuln_state in vuln_states:
            total_vulnerabilities[vuln_type][vuln_state] = []

    for vuln in vulnerabilities:
        total_vulnerabilities[vuln.type][vuln.state.status].append(vuln)

    for vuln_type in vuln_types:
        for vuln_state in vuln_states:
            grouped_vulns = vulns_utils.group_specific(
                tuple(total_vulnerabilities[vuln_type][vuln_state]),
                vuln_type,
            )
            result_vulns.extend(grouped_vulns)
    return tuple(result_vulns)


async def mask_vulnerability(
    *,
    loaders: Any,
    finding_id: str,
    vulnerability_id: str,
) -> bool:
    historic_treatment_loader = loaders.vulnerability_historic_treatment
    historic_treatment_loader.clear(vulnerability_id)
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
    vulnerabilities = await get_by_finding_and_vuln_ids(
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
    vulnerabilities = await get_by_finding_and_vuln_ids(
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
    updated_vulns: Tuple[Vulnerability, ...],
) -> None:
    translations = {"IN_PROGRESS": "In Progress"}
    if treatment in translations:
        vulns_grouped = group_vulnerabilities(updated_vulns)
        vulns_data = vulns_utils.format_vulnerabilities(vulns_grouped)
        mail_content = get_updated_manager_mail_content(vulns_data)
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
    *,
    loaders: Any,
    finding_id: str,
    vulnerability_id: str,
    modified_date: str,
) -> None:
    """Set all state and treatment dates to finding's approval date"""
    loaders.vulnerability_historic_state.clear(vulnerability_id)
    historic_state: Tuple[
        VulnerabilityState, ...
    ] = await loaders.vulnerability_historic_state.load(vulnerability_id)
    historic_state = tuple(
        state._replace(modified_date=modified_date) for state in historic_state
    )
    await vulns_dal.update_historic_state(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        historic_state=historic_state,
    )

    loaders.vulnerability_historic_treatment.clear(vulnerability_id)
    historic_treatment: Tuple[
        VulnerabilityTreatment, ...
    ] = await loaders.vulnerability_historic_treatment.load(vulnerability_id)
    historic_treatment = tuple(
        treatment._replace(modified_date=modified_date)
        for treatment in historic_treatment
    )
    await vulns_dal.update_historic_treatment(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        historic_treatment=historic_treatment,
    )


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
                vulns_utils.get_treatment_from_org_finding_policy(
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
        if vulns_utils.is_reattack_requested(vulnerability):
            await verify_vulnerability(vulnerability)
