# pylint:disable=too-many-lines
from aioextensions import (
    collect,
    schedule,
)
from custom_exceptions import (
    InvalidParameter,
    InvalidRemovalVulnState,
    RequiredFieldToBeUpdate,
    VulnNotFound,
    VulnNotInFinding,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    utils as db_model_utils,
    vulnerabilities as vulns_model,
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
from db_model.findings.enums import (
    FindingVerificationStatus,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
)
from db_model.vulnerabilities import (
    enums as vulns_enums,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
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
from finding_comments import (
    domain as comments_domain,
)
from itertools import (
    cycle,
)
import logging
import logging.config
from mailer import (
    vulnerabilities as vulns_mail,
)
from newutils import (
    datetime as datetime_utils,
    validations as validations_utils,
    vulnerabilities as vulns_utils,
)
from notifications import (
    domain as notifications_domain,
)
from sessions import (
    domain as sessions_domain,
)
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
    Iterable,
    Optional,
    Union,
)
from vulnerabilities.domain.utils import (
    get_finding,
)
from vulnerabilities.domain.validations import (
    validate_commit_hash,
    validate_lines_specific,
    validate_path,
    validate_ports_specific,
    validate_source,
    validate_uniqueness,
    validate_where,
)
from vulnerabilities.types import (
    FindingGroupedVulnerabilitiesInfo,
    GroupedVulnerabilitiesInfo,
    ToolItem,
    Treatments,
    Verifications,
    VulnerabilityDescriptionToUpdate,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_vulnerability(
    loaders: Dataloaders, vulnerability_id: str
) -> Vulnerability:
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    if vulnerability is None:
        raise VulnNotFound()

    return vulnerability


async def confirm_vulnerabilities_zero_risk(
    *,
    loaders: Dataloaders,
    vuln_ids: set[str],
    finding_id: str,
    user_info: dict[str, Any],
    justification: str,
) -> None:
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
    comment_data = FindingComment(
        finding_id=finding_id,
        content=justification,
        comment_type=CommentType.ZERO_RISK,
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=datetime_utils.get_utc_now(),
        parent_id="0",
    )
    await comments_domain.add(loaders, comment_data)
    await collect(
        vulns_model.update_historic_entry(
            current_value=vuln,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            entry=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_utc_now(),
                status=VulnerabilityZeroRiskStatus.CONFIRMED,
            ),
        )
        for vuln in vulnerabilities
    )


async def add_tags(
    vulnerability: Vulnerability,
    tags: list[str],
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
    tags: Optional[list[str]] = vulnerability.tags
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
    loaders: Dataloaders,
    vuln_ids: set[str],
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
    loaders: Dataloaders,
    finding_id: str,
    vulnerability_id: str,
    justification: VulnerabilityStateReason,
    email: str,
    include_closed_vuln: bool = False,
) -> None:
    vulnerability = await get_vulnerability(loaders, vulnerability_id)
    if vulnerability.state.status == VulnerabilityStateStatus.DELETED:
        raise VulnNotFound()
    if (
        vulnerability.state.status != VulnerabilityStateStatus.VULNERABLE
        and not include_closed_vuln
    ):
        raise InvalidRemovalVulnState.new()

    deletion_state = VulnerabilityState(
        commit=vulnerability.state.commit,
        modified_by=email,
        modified_date=datetime_utils.get_utc_now(),
        source=vulnerability.state.source,
        specific=vulnerability.state.specific,
        status=VulnerabilityStateStatus.DELETED,
        reasons=[justification],
        tool=vulnerability.state.tool,
        where=vulnerability.state.where,
    )
    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        entry=deletion_state,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
    )
    finding = await get_finding(loaders, finding_id)
    if finding.approval is None:
        await vulns_model.remove(vulnerability_id=vulnerability_id)


async def get_by_finding_and_vuln_ids(
    loaders: Dataloaders,
    finding_id: str,
    vuln_ids: set[str],
) -> tuple[Vulnerability, ...]:
    finding_vulns = await loaders.finding_vulnerabilities.load(finding_id)
    filtered_vulns = tuple(
        vuln for vuln in finding_vulns if vuln.id in vuln_ids
    )
    if len(filtered_vulns) != len(vuln_ids):
        raise VulnNotInFinding()
    return filtered_vulns


async def get_closing_date(
    vulnerability: Vulnerability,
) -> Optional[datetime]:
    """Get the closing date in ISO8601 UTC format."""
    current_closing_date = (
        vulnerability.unreliable_indicators.unreliable_closing_date
    )
    if current_closing_date:
        return current_closing_date

    if vulnerability.state.status is VulnerabilityStateStatus.SAFE:
        return vulnerability.state.modified_date

    return None


async def get_grouped_vulnerabilities_info(
    loaders: Dataloaders,
    finding_id: str,
) -> FindingGroupedVulnerabilitiesInfo:
    vulnerabilities_by_type = await get_open_vulnerabilities_specific_by_type(
        loaders, finding_id
    )
    ports_vulnerabilities = vulnerabilities_by_type["ports_vulnerabilities"]
    lines_vulnerabilities = vulnerabilities_by_type["lines_vulnerabilities"]
    inputs_vulnerabilities = vulnerabilities_by_type["inputs_vulnerabilities"]
    grouped_ports_vulnerabilities: tuple[
        GroupedVulnerabilitiesInfo, ...
    ] = tuple()
    grouped_inputs_vulnerabilities: tuple[
        GroupedVulnerabilitiesInfo, ...
    ] = tuple()
    grouped_lines_vulnerabilities: tuple[
        GroupedVulnerabilitiesInfo, ...
    ] = tuple()
    where = "-"
    if ports_vulnerabilities:
        grouped_ports_vulnerabilities = tuple(
            map(
                lambda grouped_vulns_info: GroupedVulnerabilitiesInfo(
                    where=grouped_vulns_info.state.where,
                    specific=grouped_vulns_info.state.specific,
                    commit_hash=grouped_vulns_info.state.commit
                    if grouped_vulns_info.state.commit is not None
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
                    where=grouped_vulns_info.state.where,
                    specific=grouped_vulns_info.state.specific,
                    commit_hash=grouped_vulns_info.state.commit
                    if grouped_vulns_info.state.commit is not None
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
                    where=grouped_vulns_info.state.where,
                    specific=grouped_vulns_info.state.specific,
                    commit_hash=grouped_vulns_info.state.commit
                    if grouped_vulns_info.state.commit is not None
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
    loaders: Dataloaders,
    finding_id: str,
) -> dict[str, tuple[Vulnerability, ...]]:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(tuple(vulns))
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
    vulnerabilities: Iterable[Vulnerability],
) -> Treatments:
    treatment_counter = Counter(
        vuln.treatment.status
        for vuln in vulnerabilities
        if vuln.treatment
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    return Treatments(
        accepted=treatment_counter[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment_counter[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        in_progress=treatment_counter[
            VulnerabilityTreatmentStatus.IN_PROGRESS
        ],
        untreated=treatment_counter[VulnerabilityTreatmentStatus.UNTREATED],
    )


def get_verifications_count(
    vulnerabilities: tuple[Vulnerability, ...],
) -> Verifications:
    treatment_counter = Counter(
        vuln.verification.status
        for vuln in vulnerabilities
        if vuln.verification
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )
    return Verifications(
        requested=treatment_counter[VulnerabilityVerificationStatus.REQUESTED],
        on_hold=treatment_counter[VulnerabilityVerificationStatus.ON_HOLD],
        verified=treatment_counter[VulnerabilityVerificationStatus.VERIFIED],
    )


def group_vulnerabilities(
    vulnerabilities: tuple[Vulnerability, ...]
) -> tuple[Vulnerability, ...]:
    """Group vulnerabilities by specific field."""
    vuln_types = (
        VulnerabilityType.LINES,
        VulnerabilityType.PORTS,
        VulnerabilityType.INPUTS,
    )
    vuln_states = (
        VulnerabilityStateStatus.VULNERABLE,
        VulnerabilityStateStatus.SAFE,
    )
    total_vulnerabilities: dict[str, dict[str, list[Vulnerability]]] = {}
    result_vulns: list[Vulnerability] = []
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
    loaders: Dataloaders,
    email: str,
    finding_id: str,
    vulnerability: Vulnerability,
) -> None:
    finding = await get_finding(loaders, finding_id)
    if (
        vulnerability.state.status == VulnerabilityStateStatus.DELETED
        and finding.approval
    ):
        # Vulnerabilities in the MASKED state will be archived by Streams
        # for analytics purposes
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            entry=vulnerability.state._replace(
                modified_by=email,
                modified_date=datetime_utils.get_utc_now(),
                status=VulnerabilityStateStatus.MASKED,
            ),
            finding_id=finding_id,
            vulnerability_id=vulnerability.id,
        )
    await vulns_model.remove(vulnerability_id=vulnerability.id)


async def confirm_vulnerabilities(
    *,
    loaders: Dataloaders,
    vuln_ids: set[str],
    finding_id: str,
    modified_by: str,
) -> None:
    vulnerabilities = await get_by_finding_and_vuln_ids(
        loaders, finding_id, vuln_ids
    )
    for vulnerability in vulnerabilities:
        vulns_utils.validate_submitted(vulnerability)

    await collect(
        tuple(
            vulns_model.update_historic_entry(
                current_value=vulnerability,
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=vulnerability.state._replace(
                    modified_by=modified_by,
                    modified_date=datetime_utils.get_utc_now(),
                    status=VulnerabilityStateStatus.VULNERABLE,
                ),
            )
            for vulnerability in vulnerabilities
        )
    )


async def reject_vulnerabilities(
    *,
    loaders: Dataloaders,
    vuln_ids: set[str],
    finding_id: str,
    modified_by: str,
    reasons: set[VulnerabilityStateReason],
    other_reason: Optional[str],
) -> None:
    if VulnerabilityStateReason.OTHER not in reasons and other_reason:
        InvalidParameter("justification")
    if VulnerabilityStateReason.OTHER in reasons and not other_reason:
        InvalidParameter("other_reason")
    if other_reason is not None:
        vulns_utils.validate_justification_length(other_reason)
    vulnerabilities = await get_by_finding_and_vuln_ids(
        loaders, finding_id, vuln_ids
    )
    for vulnerability in vulnerabilities:
        vulns_utils.validate_submitted(vulnerability)

    await collect(
        tuple(
            vulns_model.update_historic_entry(
                current_value=vulnerability,
                finding_id=vulnerability.finding_id,
                vulnerability_id=vulnerability.id,
                entry=vulnerability.state._replace(
                    modified_by=modified_by,
                    modified_date=datetime_utils.get_utc_now(),
                    status=VulnerabilityStateStatus.REJECTED,
                    reasons=list(reasons),
                    other_reason=other_reason,
                ),
            )
            for vulnerability in vulnerabilities
        )
    )


async def reject_vulnerabilities_zero_risk(
    *,
    loaders: Dataloaders,
    vuln_ids: set[str],
    finding_id: str,
    user_info: dict[str, Any],
    justification: str,
) -> None:
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
    comment_data = FindingComment(
        finding_id=finding_id,
        content=justification,
        comment_type=CommentType.ZERO_RISK,
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=datetime_utils.get_utc_now(),
        parent_id="0",
    )
    await comments_domain.add(loaders, comment_data)
    await collect(
        vulns_model.update_historic_entry(
            current_value=vuln,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            entry=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=user_email,
                modified_date=datetime_utils.get_utc_now(),
                status=VulnerabilityZeroRiskStatus.REJECTED,
            ),
        )
        for vuln in vulnerabilities
    )


async def request_verification(vulnerability: Vulnerability) -> None:
    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=VulnerabilityVerification(
            modified_date=datetime_utils.get_utc_now(),
            status=VulnerabilityVerificationStatus.REQUESTED,
        ),
    )


async def request_hold(event_id: str, vulnerability: Vulnerability) -> None:
    verification = VulnerabilityVerification(
        event_id=event_id,
        modified_date=datetime_utils.get_utc_now(),
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


async def request_vulnerabilities_zero_risk(
    *,
    loaders: Dataloaders,
    vuln_ids: set[str],
    finding_id: str,
    user_info: dict[str, Any],
    justification: str,
) -> None:
    vulns_utils.validate_justification_length(justification)
    vulnerabilities = await get_by_finding_and_vuln_ids(
        loaders, finding_id, vuln_ids
    )
    for vuln in vulnerabilities:
        vulns_utils.validate_non_zero_risk_requested(vuln)
        vulns_utils.validate_released(vuln)
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    user_email = user_info["user_email"]
    comment_data = FindingComment(
        finding_id=finding_id,
        content=justification,
        comment_type=CommentType.ZERO_RISK,
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=datetime_utils.get_utc_now(),
        parent_id="0",
    )
    await comments_domain.add(loaders, comment_data)
    await collect(
        vulns_model.update_historic_entry(
            current_value=vuln,
            finding_id=vuln.finding_id,
            vulnerability_id=vuln.id,
            entry=VulnerabilityZeroRisk(
                comment_id=comment_id,
                modified_by=str(user_email),
                modified_date=datetime_utils.get_utc_now(),
                status=VulnerabilityZeroRiskStatus.REQUESTED,
            ),
        )
        for vuln in vulnerabilities
    )
    await notifications_domain.request_vulnerability_zero_risk(
        loaders=loaders,
        finding_id=finding_id,
        justification=justification,
        requester_email=str(user_email),
        vulnerabilities=vulnerabilities,
    )


def get_updated_manager_mail_content(
    vulnerabilities: dict[str, list[dict[str, Union[str, ToolItem]]]]
) -> str:
    mail_content = ""
    for vuln_type in ["ports", "lines", "inputs"]:
        type_vulns = vulnerabilities.get(vuln_type)
        if type_vulns:
            mail_content += "\n".join(
                [
                    f"{list(vuln.values())[0]} ({list(vuln.values())[1]})"
                    for vuln in type_vulns
                ]
            )
            mail_content += "\n"
    return mail_content


async def should_send_update_treatment(
    *,
    loaders: Dataloaders,
    assigned: str,
    finding_id: str,
    finding_title: str,
    group_name: str,
    justification: str,
    treatment: str,
    updated_vulns: tuple[Vulnerability, ...],
    modified_by: str,
) -> None:
    translations: dict[str, str] = {
        "IN_PROGRESS": "In progress",
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
    loaders: Dataloaders,
    finding_id: str,
    vulnerability_id: str,
    modified_date: datetime,
) -> None:
    """Set all state and treatment dates to finding's approval date."""
    loaders.vulnerability_historic_state.clear(vulnerability_id)
    historic_state = await loaders.vulnerability_historic_state.load(
        vulnerability_id
    )
    historic_state = cast(
        tuple[VulnerabilityState, VulnerabilityState],
        db_model_utils.adjust_historic_dates(
            tuple(
                state._replace(modified_date=modified_date)
                for state in historic_state
            )
        ),
    )
    loaders.vulnerability.clear(vulnerability_id)
    vulnerability = await get_vulnerability(loaders, vulnerability_id)
    await vulns_model.update_historic(
        current_value=vulnerability,
        historic=historic_state,
    )
    await vulns_model.update_metadata(
        finding_id=finding_id,
        metadata=VulnerabilityMetadataToUpdate(
            created_date=historic_state[0].modified_date
        ),
        vulnerability_id=vulnerability_id,
    )

    loaders.vulnerability_historic_treatment.clear(vulnerability_id)
    historic_treatment = await loaders.vulnerability_historic_treatment.load(
        vulnerability_id
    )
    historic_treatment = cast(
        tuple[VulnerabilityTreatment, VulnerabilityTreatment],
        db_model_utils.adjust_historic_dates(
            tuple(
                treatment._replace(modified_date=modified_date)
                for treatment in historic_treatment
            )
        ),
    )
    loaders.vulnerability.clear(vulnerability_id)
    vulnerability = await get_vulnerability(loaders, vulnerability_id)
    await vulns_model.update_historic(
        current_value=vulnerability,
        historic=historic_treatment,
    )


async def update_metadata(
    *,
    loaders: Dataloaders,
    vulnerability_id: str,
    finding_id: str,
    bug_tracking_system_url: Optional[str],
    custom_severity: Optional[int],
    tags_to_append: Optional[list[str]],
) -> None:
    vulnerability = await get_vulnerability(loaders, vulnerability_id)
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
    finding_policy: Optional[OrgFindingPolicy] = None,
) -> str:
    """Update vulnerability metadata and historics."""
    if (
        vulnerability.state.source != new_state.source
        and vulnerability.state.status == VulnerabilityStateStatus.SAFE
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
                reasons=vulnerability.state.reasons,
                tool=vulnerability.state.tool,
                commit=vulnerability.state.commit,
                where=vulnerability.state.where,
                specific=vulnerability.state.specific,
            ),
        )
    elif (
        vulnerability.state.status != new_state.status
        or (
            vulnerability.state.tool != new_state.tool
            and vulnerability.state.status
            == VulnerabilityStateStatus.VULNERABLE
        )
        or vulnerability.state.source != new_state.source
    ):
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            entry=new_state,
        )

    if (  # pylint: disable=too-many-boolean-expressions
        vulnerability.state.status != new_state.status
        and finding_policy
        and new_state.status == VulnerabilityStateStatus.VULNERABLE
        and finding_policy.state.status == PolicyStateStatus.APPROVED
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
    loaders: Dataloaders,
    modified_date: datetime,
    closed_vulns_ids: list[str],
    vulns_to_close_from_file: list[Vulnerability],
    context: Optional[Any] = None,
) -> None:
    list_closed_vulns: list[Vulnerability] = []
    for vuln_id in sorted(closed_vulns_ids):
        loaders.vulnerability.clear(vuln_id)
        list_closed_vulns.append(await get_vulnerability(loaders, vuln_id))

    if context:
        user_data = await sessions_domain.get_jwt_content(context)
        modified_by = str(user_data["user_email"])
    else:
        modified_by = "machine@fluidattacks.com"

    await collect(
        update_metadata_and_state(
            vulnerability=vuln_to_close,
            new_metadata=VulnerabilityMetadataToUpdate(
                stream=(
                    close_item.stream
                    if close_item
                    and close_item.type == VulnerabilityType.INPUTS
                    else None
                ),
            ),
            new_state=VulnerabilityState(
                commit=close_item.state.commit
                if close_item and close_item.type == VulnerabilityType.LINES
                else None
                if close_item and close_item.type != VulnerabilityType.LINES
                else vuln_to_close.state.commit,
                modified_by=modified_by,
                modified_date=modified_date,
                other_reason=vuln_to_close.state.other_reason,
                reasons=vuln_to_close.state.reasons,
                source=vuln_to_close.state.source,
                specific=vuln_to_close.state.specific,
                status=VulnerabilityStateStatus.SAFE,
                tool=close_item.state.tool
                if close_item
                else vuln_to_close.state.tool,
                where=vuln_to_close.state.where,
            ),
        )
        for vuln_to_close, close_item in zip(
            list_closed_vulns,
            vulns_to_close_from_file or cycle([None]),
        )
    )


async def verify_vulnerability(vulnerability: Vulnerability) -> None:
    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=VulnerabilityVerification(
            modified_date=datetime_utils.get_utc_now(),
            status=VulnerabilityVerificationStatus.VERIFIED,
        ),
    )


async def close_by_exclusion(
    vulnerability: Vulnerability,
    modified_by: str,
) -> None:
    if vulnerability.state.status not in {
        VulnerabilityStateStatus.SAFE,
        VulnerabilityStateStatus.DELETED,
        VulnerabilityStateStatus.MASKED,
    }:
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            entry=VulnerabilityState(
                commit=vulnerability.state.commit,
                modified_by=modified_by,
                modified_date=datetime_utils.get_utc_now(),
                source=vulnerability.state.source,
                specific=vulnerability.state.specific,
                status=VulnerabilityStateStatus.SAFE,
                reasons=[VulnerabilityStateReason.EXCLUSION],
                where=vulnerability.state.where,
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
                        modified_date=datetime_utils.get_utc_now(),
                        status=VulnerabilityVerificationStatus.VERIFIED,
                        event_id=None,
                    ),
                    vulnerability_id=vulnerability.id,
                    delete_index=True,
                )


async def get_reattack_requester(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> Optional[str]:
    historic_verification = await loaders.finding_historic_verification.load(
        vuln.finding_id
    )
    reversed_historic_verification = list(reversed(historic_verification))
    for verification in reversed_historic_verification:
        if (
            verification.status == FindingVerificationStatus.REQUESTED
            and verification.vulnerability_ids is not None
            and vuln.id in verification.vulnerability_ids
        ):
            return verification.modified_by

    return None


async def get_last_requested_reattack_date(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> Optional[datetime]:
    if not vuln.verification:
        return None
    if vuln.verification.status == VulnerabilityVerificationStatus.REQUESTED:
        return vuln.verification.modified_date

    historic = await loaders.vulnerability_historic_verification.load(vuln.id)

    return next(
        (
            verification.modified_date
            for verification in reversed(historic)
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ),
        None,
    )


async def get_last_reattack_date(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> Optional[datetime]:
    if not vuln.verification:
        return None
    if vuln.verification.status == VulnerabilityVerificationStatus.VERIFIED:
        return vuln.verification.modified_date

    historic = await loaders.vulnerability_historic_verification.load(vuln.id)

    return next(
        (
            verification.modified_date
            for verification in reversed(historic)
            if verification.status == VulnerabilityVerificationStatus.VERIFIED
        ),
        None,
    )


async def update_description(  # noqa: MC0001 # NOSONAR
    loaders: Dataloaders,
    vulnerability_id: str,
    description: VulnerabilityDescriptionToUpdate,
    stakeholder_email: str,
) -> None:
    if all(attribute is None for attribute in description):
        raise RequiredFieldToBeUpdate()

    vulnerability = await get_vulnerability(loaders, vulnerability_id)
    updated_commit = validate_and_get_updated_commit(
        vulnerability, description
    )
    updated_specific = validate_and_get_updated_specific(
        vulnerability, description
    )
    updated_source = validate_and_get_updated_source(
        vulnerability, description
    )
    updated_where = validate_and_get_updated_where(vulnerability, description)

    if any([description.specific is not None, description.where is not None]):
        vulnerabilities_connection: VulnerabilitiesConnection = (
            await loaders.finding_vulnerabilities_released_nzr_c.load(
                FindingVulnerabilitiesZrRequest(
                    finding_id=vulnerability.finding_id,
                    paginate=False,
                    state_status=VulnerabilityStateStatus.VULNERABLE,
                )
            )
        )
        zr_vulnerabilities_connection: VulnerabilitiesConnection = (
            await loaders.finding_vulnerabilities_released_zr_c.load(
                FindingVulnerabilitiesZrRequest(
                    finding_id=vulnerability.finding_id,
                    paginate=False,
                    state_status=VulnerabilityStateStatus.VULNERABLE,
                )
            )
        )
        validate_uniqueness(
            finding_vulns_data=tuple(
                edge.node
                for edge in vulnerabilities_connection.edges
                + zr_vulnerabilities_connection.edges
                if edge.node.id != vulnerability.id
            ),
            vulnerability_where=updated_where,
            vulnerability_specific=updated_specific,
            vulnerability_type=vulnerability.type,
            vulnerability_id=vulnerability_id,
        )
        await vulns_utils.validate_vulnerability_in_toe(
            loaders,
            vulnerability._replace(
                state=vulnerability.state._replace(
                    commit=updated_commit,
                    specific=updated_specific,
                    source=updated_source,
                    where=updated_where,
                ),
            ),
            index=0,
        )

    if not (
        updated_commit == vulnerability.state.commit
        and updated_source == vulnerability.state.source
        and updated_specific == vulnerability.state.specific
        and updated_where == vulnerability.state.where
    ):
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            entry=vulnerability.state._replace(
                commit=updated_commit,
                modified_by=stakeholder_email,
                modified_date=datetime_utils.get_utc_now(),
                source=updated_source,
                specific=updated_specific,
                where=updated_where,
            ),
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
        )


def validate_and_get_updated_commit(
    vulnerability: Vulnerability, description: VulnerabilityDescriptionToUpdate
) -> Optional[str]:
    if description.commit is not None:
        if vulnerability.type is not VulnerabilityType.LINES:
            raise InvalidParameter("commit")
        validate_commit_hash(description.commit)
        return description.commit
    return vulnerability.state.commit


def validate_and_get_updated_specific(
    vulnerability: Vulnerability, description: VulnerabilityDescriptionToUpdate
) -> str:
    if description.specific is not None:
        validations_utils.validate_sanitized_csv_input(description.specific)
        if vulnerability.type is VulnerabilityType.LINES:
            validate_lines_specific(description.specific)
        if vulnerability.type is VulnerabilityType.PORTS:
            validate_ports_specific(description.specific)
        return description.specific
    return vulnerability.state.specific


def validate_and_get_updated_source(
    vulnerability: Vulnerability, description: VulnerabilityDescriptionToUpdate
) -> Source:
    if description.source is not None:
        validate_source(description.source)
        return description.source
    return vulnerability.state.source


def validate_and_get_updated_where(
    vulnerability: Vulnerability, description: VulnerabilityDescriptionToUpdate
) -> str:
    if description.where is not None:
        if vulnerability.type is VulnerabilityType.LINES:
            validate_path(description.where)
        validate_where(description.where)
        return description.where
    return vulnerability.state.where
