# pylint:disable=too-many-lines
from aioextensions import (
    collect,
    schedule,
)
from comments import (
    domain as comments_domain,
)
from custom_exceptions import (
    InvalidRemovalVulnState,
    VulnNotFound,
    VulnNotInFinding,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    FindingVerification,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from db_model.vulnerabilities.update import (
    update_event_index,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
)
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
    requests as requests_utils,
    token as token_utils,
    vulnerabilities as vulns_utils,
)
from notifications import (
    domain as notifications_domain,
)
import redshift.vulnerabilities as redshift_vulns
from settings import (
    LOGGING,
)
from time import (
    time,
)
from typing import (
    Any,
    cast,
    Counter,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)
from vulnerabilities.types import (
    FindingGroupedVulnerabilitiesInfo,
    GroupedVulnerabilitiesInfo,
    Treatments,
    Verifications,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _send_to_redshift(
    *,
    loaders: Any,
    vulnerability: Vulnerability,
) -> None:
    historic_state = await loaders.vulnerability_historic_state.load(
        vulnerability.id
    )
    historic_treatment = await loaders.vulnerability_historic_treatment.load(
        vulnerability.id
    )
    historic_verification = (
        await loaders.vulnerability_historic_verification.load(
            vulnerability.id
        )
    )
    historic_zero_risk = await loaders.vulnerability_historic_zero_risk.load(
        vulnerability.id
    )
    await redshift_vulns.insert_vulnerability(
        vulnerability=vulnerability,
        historic_state=historic_state,
        historic_treatment=historic_treatment,
        historic_verification=historic_verification,
        historic_zero_risk=historic_zero_risk,
    )
    LOGGER.info(
        "Vulnerability stored in redshift",
        extra={
            "extra": {
                "vulnerability_id": vulnerability.id,
                "finding_id": vulnerability.finding_id,
            }
        },
    )


async def confirm_vulnerabilities_zero_risk(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    user_info: Dict[str, Any],
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
    user_email = str(user_info["user_email"])
    comment_data: Dict[str, Any] = {
        "comment_type": "zero_risk",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }

    stakeholder = Stakeholder(
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        email=user_email,
    )
    add_comment = await comments_domain.add(
        finding_id, comment_data, stakeholder
    )
    await collect(
        vulns_model.update_historic_entry(
            current_value=vuln,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            entry=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                status=VulnerabilityZeroRiskStatus.CONFIRMED,
            ),
        )
        for vuln in vulnerabilities
    )
    if not add_comment[1]:
        LOGGER.error("An error occurred confirming zero risk vuln")
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
    await vulns_model.update_metadata(
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        metadata=VulnerabilityMetadataToUpdate(
            tags=sorted(list(set(tags))),
        ),
    )


async def _remove_all_tags(
    vulnerability: Vulnerability,
) -> None:
    await vulns_model.update_metadata(
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
        await vulns_model.update_metadata(
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
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        vulnerability_id
    )
    if (
        vulnerability.state.status != VulnerabilityStateStatus.OPEN
        and not include_closed_vuln
    ):
        raise InvalidRemovalVulnState.new()

    finding: Finding = await loaders.finding.load(finding_id)
    if (
        not user_email.endswith("@fluidattacks.com")
        and finding.state.status == FindingStateStatus.APPROVED
    ):
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            entry=VulnerabilityState(
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                source=source,
                status=VulnerabilityStateStatus.DELETED,
                justification=justification,
            ),
            finding_id=finding_id,
            vulnerability_id=vulnerability_id,
        )
        await _send_to_redshift(
            loaders=loaders,
            vulnerability=vulnerability,
        )
    await vulns_model.remove(vulnerability_id=vulnerability_id)
    return True


async def get_by_finding_and_vuln_ids(
    loaders: Any,
    finding_id: str,
    vuln_ids: Set[str],
) -> Tuple[Vulnerability, ...]:
    finding_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load(finding_id)
    filtered_vulns = tuple(
        vuln for vuln in finding_vulns if vuln.id in vuln_ids
    )
    if len(filtered_vulns) != len(vuln_ids):
        raise VulnNotInFinding()
    return filtered_vulns


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
    ] = await loaders.finding_vulnerabilities_nzr.load(finding_id)
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


def get_verifications_count(
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Verifications:
    treatment_counter = Counter(
        vuln.verification.status
        for vuln in vulnerabilities
        if vuln.verification
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    return Verifications(
        requested=treatment_counter[VulnerabilityVerificationStatus.REQUESTED],
        on_hold=treatment_counter[VulnerabilityVerificationStatus.ON_HOLD],
        verified=treatment_counter[VulnerabilityVerificationStatus.VERIFIED],
    )


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
    result_vulns: List[Vulnerability] = []
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
    vulnerability: Vulnerability,
) -> None:
    store_vuln: bool = True
    if vulnerability.state.status == VulnerabilityStateStatus.DELETED:
        finding: Finding = await loaders.finding.load(finding_id)
        if (
            vulnerability.state.modified_by.endswith("@fluidattacks.com")
            or finding.state.status != FindingStateStatus.APPROVED
        ):
            store_vuln = False

    if store_vuln:
        await _send_to_redshift(
            loaders=loaders,
            vulnerability=vulnerability,
        )
    await vulns_model.remove(vulnerability_id=vulnerability.id)


async def reject_vulnerabilities_zero_risk(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    user_info: Dict[str, Any],
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
    user_email = str(user_info["user_email"])
    comment_data: Dict[str, Any] = {
        "comment_type": "zero_risk",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    stakeholder = Stakeholder(
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        email=user_email,
    )
    add_comment = await comments_domain.add(
        finding_id, comment_data, stakeholder
    )
    await collect(
        vulns_model.update_historic_entry(
            current_value=vuln,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            entry=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                status=VulnerabilityZeroRiskStatus.REJECTED,
            ),
        )
        for vuln in vulnerabilities
    )
    if not add_comment[1]:
        LOGGER.error("An error occurred rejecting zero risk vuln")
        return False
    return True


async def request_verification(vulnerability: Vulnerability) -> bool:
    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=VulnerabilityVerification(
            modified_date=datetime_utils.get_iso_date(),
            status=VulnerabilityVerificationStatus.REQUESTED,
        ),
    )
    return True


async def request_hold(event_id: str, vulnerability: Vulnerability) -> bool:
    verification = VulnerabilityVerification(
        event_id=event_id,
        modified_date=datetime_utils.get_iso_date(),
        status=VulnerabilityVerificationStatus.ON_HOLD,
    )
    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=verification,
    )
    await vulns_model.update_event_index(
        finding_id=vulnerability.finding_id,
        entry=verification,
        vulnerability_id=vulnerability.id,
    )
    return True


async def request_vulnerabilities_zero_risk(
    *,
    loaders: Any,
    vuln_ids: Set[str],
    finding_id: str,
    user_info: Dict[str, Any],
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
    comment_data: Dict[str, Any] = {
        "comment_type": "zero_risk",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    stakeholder = Stakeholder(
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        email=user_email,
    )
    add_comment = await comments_domain.add(
        finding_id, comment_data, stakeholder
    )
    await collect(
        vulns_model.update_historic_entry(
            current_value=vuln,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            entry=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=str(user_email),
                modified_date=datetime_utils.get_iso_date(),
                status=VulnerabilityZeroRiskStatus.REQUESTED,
            ),
        )
        for vuln in vulnerabilities
    )
    if not add_comment[1]:
        LOGGER.error("An error occurred requesting zero risk vuln")
        return False
    await notifications_domain.request_vulnerability_zero_risk(
        loaders=loaders,
        finding_id=finding_id,
        justification=justification,
        requester_email=str(user_email),
        vulnerabilities=vulnerabilities,
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
    assigned: str,
    finding_id: str,
    finding_title: str,
    group_name: str,
    justification: str,
    treatment: str,
    updated_vulns: Tuple[Vulnerability, ...],
    modified_by: str,
) -> None:
    translations: dict[str, str] = {
        "IN_PROGRESS": "In Progress",
        "ACCEPTED": "Temporarily accepted",
    }
    if treatment in translations:
        vulns_grouped = group_vulnerabilities(updated_vulns)
        vulns_data = await vulns_utils.format_vulnerabilities(
            group_name, loaders, vulns_grouped
        )
        mail_content = get_updated_manager_mail_content(vulns_data)
        schedule(
            vulns_mail.send_mail_updated_treatment(
                loaders=loaders,
                assigned=assigned,
                finding_id=finding_id,
                finding_title=finding_title,
                group_name=group_name,
                justification=justification,
                treatment=translations[treatment],
                vulnerabilities=mail_content,
                modified_by=modified_by,
            )
        )


async def update_historics_dates(
    *,
    loaders: Any,
    vulnerability_id: str,
    modified_date: str,
) -> None:
    """Set all state and treatment dates to finding's approval date."""
    loaders.vulnerability_historic_state.clear(vulnerability_id)
    historic_state: Tuple[
        VulnerabilityState, ...
    ] = await loaders.vulnerability_historic_state.load(vulnerability_id)
    historic_state = cast(
        Tuple[VulnerabilityState, VulnerabilityState],
        vulns_model.utils.adjust_historic_dates(
            tuple(
                state._replace(modified_date=modified_date)
                for state in historic_state
            )
        ),
    )
    loaders.vulnerability.clear(vulnerability_id)
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    await vulns_model.update_historic(
        current_value=vulnerability,
        historic=historic_state,
    )

    loaders.vulnerability_historic_treatment.clear(vulnerability_id)
    historic_treatment: Tuple[
        VulnerabilityTreatment, ...
    ] = await loaders.vulnerability_historic_treatment.load(vulnerability_id)
    historic_treatment = cast(
        Tuple[VulnerabilityTreatment, VulnerabilityTreatment],
        vulns_model.utils.adjust_historic_dates(
            tuple(
                treatment._replace(modified_date=modified_date)
                for treatment in historic_treatment
            )
        ),
    )
    loaders.vulnerability.clear(vulnerability_id)
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    await vulns_model.update_historic(
        current_value=vulnerability,
        historic=historic_treatment,
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
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        vulnerability_id
    )
    all_tags = []
    if vulnerability.tags:
        all_tags.extend(vulnerability.tags)
    if tags_to_append:
        all_tags.extend(tags_to_append)
    await vulns_model.update_metadata(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        metadata=VulnerabilityMetadataToUpdate(
            bug_tracking_system_url=bug_tracking_system_url,
            custom_severity=""
            if custom_severity is None or custom_severity <= 0
            else str(custom_severity),
            tags=sorted(list(set(all_tags))),
        ),
    )


async def update_metadata_and_state(
    *,
    vulnerability: Vulnerability,
    new_metadata: VulnerabilityMetadataToUpdate,
    new_state: VulnerabilityState,
    finding_policy: Optional[OrgFindingPolicyItem] = None,
) -> str:
    """Update vulnerability metadata and historics."""
    if (
        vulnerability.state.source != new_state.source
        or vulnerability.state.status != new_state.status
    ):
        if (
            vulnerability.state.source != new_state.source
            and vulnerability.state.status == VulnerabilityStateStatus.CLOSED
        ):
            await vulns_model.update_historic_entry(
                current_value=vulnerability,
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=VulnerabilityState(
                    modified_by=vulnerability.state.modified_by,
                    modified_date=vulnerability.state.modified_date,
                    source=new_state.source,
                    status=vulnerability.state.status,
                    justification=vulnerability.state.justification,
                ),
            )
        else:
            await vulns_model.update_historic_entry(
                current_value=vulnerability,
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=new_state,
            )
        if (
            finding_policy
            and new_state.status == VulnerabilityStateStatus.OPEN
            and finding_policy.state.status == "APPROVED"
            and vulnerability.treatment
            and vulnerability.treatment.status
            != VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ):
            treatment_to_update = (
                vulns_utils.get_treatment_from_org_finding_policy(
                    modified_date=new_state.modified_date,
                    user_email=finding_policy.state.modified_by,
                )
            )
            await vulns_model.update_treatment(
                current_value=vulnerability,
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                treatment=treatment_to_update[0],
            )
            await vulns_model.update_treatment(
                current_value=vulnerability._replace(
                    treatment=treatment_to_update[0]
                ),
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                treatment=treatment_to_update[1],
            )

    await vulns_model.update_metadata(
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        metadata=new_metadata,
    )
    return vulnerability.id


async def verify(
    *,
    context: Any,
    modified_date: str,
    closed_vulns_ids: List[str],
    vulns_to_close_from_file: List[Vulnerability],
) -> bool:
    for vuln_id in closed_vulns_ids:
        context.loaders.vulnerability.clear(vuln_id)

    list_closed_vulns: List[
        Vulnerability
    ] = await context.loaders.vulnerability.load_many(sorted(closed_vulns_ids))
    source: Source = requests_utils.get_source_new(context)
    user_data = await token_utils.get_jwt_content(context)
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
    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=VulnerabilityVerification(
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
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            entry=VulnerabilityState(
                modified_by=modified_by,
                modified_date=datetime_utils.get_iso_date(),
                source=source,
                status=VulnerabilityStateStatus.CLOSED,
                justification=StateRemovalJustification.EXCLUSION,
            ),
        )
        if vulns_utils.is_reattack_requested(
            vulnerability
        ) or vulns_utils.is_reattack_on_hold(vulnerability):
            await verify_vulnerability(vulnerability)
            # If the root was deactivated/moved, we need to remove the on_hold
            # status from vulns and remove them from the corresponding Event
            if vulnerability.event_id is not None:
                await update_event_index(
                    finding_id=vulnerability.finding_id,
                    entry=VulnerabilityVerification(
                        modified_date=datetime_utils.get_iso_date(),
                        status=VulnerabilityVerificationStatus.VERIFIED,
                        event_id=None,
                    ),
                    vulnerability_id=vulnerability.id,
                    delete_index=True,
                )


async def get_reattack_requester(
    loaders: Any,
    vuln: Vulnerability,
) -> Optional[str]:
    historic_verification: Tuple[
        FindingVerification, ...
    ] = await loaders.finding_historic_verification.load(vuln.finding_id)
    reversed_historic_verification = tuple(reversed(historic_verification))
    for verification in reversed_historic_verification:
        if (
            verification.status == FindingVerificationStatus.REQUESTED
            and verification.vulnerability_ids is not None
            and vuln.id in verification.vulnerability_ids
        ):
            return verification.modified_by
    return None


async def get_last_requested_reattack_date(
    loaders: Any,
    vuln: Vulnerability,
) -> Optional[str]:
    """Get last requested reattack date in ISO8601 UTC format."""
    if not vuln.verification:
        return None
    if vuln.verification.status == VulnerabilityVerificationStatus.REQUESTED:
        return vuln.verification.modified_date
    historic: Tuple[
        VulnerabilityVerification, ...
    ] = await loaders.vulnerability_historic_verification.load(vuln.id)
    return next(
        (
            verification.modified_date
            for verification in reversed(historic)
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ),
        None,
    )


async def get_last_reattack_date(
    loaders: Any,
    vuln: Vulnerability,
) -> Optional[str]:
    """Get last reattack date in ISO8601 UTC format."""
    if not vuln.verification:
        return None
    if vuln.verification.status == VulnerabilityVerificationStatus.VERIFIED:
        return vuln.verification.modified_date
    historic: Tuple[
        VulnerabilityVerification, ...
    ] = await loaders.vulnerability_historic_verification.load(vuln.id)
    return next(
        (
            verification.modified_date
            for verification in reversed(historic)
            if verification.status == VulnerabilityVerificationStatus.VERIFIED
        ),
        None,
    )


async def get_report_date(
    loaders: Any,
    vuln: Vulnerability,
) -> str:
    historic: Tuple[
        VulnerabilityState, ...
    ] = await loaders.vulnerability_historic_state.load(vuln.id)
    return historic[0].modified_date
