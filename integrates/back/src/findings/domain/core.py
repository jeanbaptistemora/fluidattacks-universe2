from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
from back.src.machine.availability import (
    operation_can_be_executed,
)
from comments import (
    domain as comments_domain,
)
from custom_exceptions import (
    InvalidCommentParent,
    MachineCanNotOperate,
    NotVerificationRequested,
    PermissionDenied,
    VulnNotFound,
)
from custom_types import (
    Comment as CommentType,
    Tracking as TrackingItem,
    User as UserType,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
    MASKED,
)
from db_model.enums import (
    StateRemovalJustification,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidences,
    FindingMetadataToUpdate,
    FindingState,
    FindingVerification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from findings import (
    storage as findings_storage,
)
from findings.types import (
    FindingDescriptionToUpdate,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from mailer import (
    findings as findings_mail,
)
import newrelic.agent
from newutils import (
    cvss_new,
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from settings import (
    LOGGING,
    NOEXTRA,
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
    Union,
)
from users import (
    domain as users_domain,
)
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.types import (
    Treatments,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: CommentType,
    finding_id: str,
    group_name: str,
) -> bool:
    param_type = comment_data.get("comment_type")
    parent = str(comment_data["parent"])
    content = str(comment_data["content"])

    await authz.validate_handle_comment_scope(
        content, user_email, group_name, parent, info.context.store
    )

    if param_type == "observation":
        enforcer = await authz.get_group_level_enforcer(
            user_email, info.context.store
        )
        if not enforcer(group_name, "post_finding_observation"):
            raise PermissionDenied()

    if parent != "0":
        finding_comments = [
            comment["comment_id"]
            for comment in await comments_domain.get(
                str(comment_data.get("comment_type")), finding_id
            )
        ]
        if parent not in finding_comments:
            raise InvalidCommentParent()

    user_data = await users_domain.get(user_email)
    user_data["user_email"] = user_data.pop("email")
    success = await comments_domain.add(finding_id, comment_data, user_data)
    return success[1]


async def remove_finding(
    context: Any,
    finding_id: str,
    justification: StateRemovalJustification,
    user_email: str,
) -> None:
    finding_loader = context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    new_state = FindingState(
        justification=justification,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.DELETED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
    schedule(
        remove_vulnerabilities(context, finding_id, justification, user_email)
    )
    file_names = await findings_storage.search_evidence(
        f"{finding.group_name}/{finding.id}"
    )
    await collect(
        findings_storage.remove_evidence(file_name) for file_name in file_names
    )
    metadata = FindingMetadataToUpdate(evidences=FindingEvidences())
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )
    await findings_model.remove(
        group_name=finding.group_name, finding_id=finding.id
    )


async def remove_vulnerabilities(
    context: Any,
    finding_id: str,
    justification: StateRemovalJustification,
    user_email: str,
) -> bool:
    finding_vulns_loader = context.loaders.finding_vulns_typed
    vulnerabilities: Tuple[Vulnerability] = await finding_vulns_loader.load(
        finding_id
    )
    source = requests_utils.get_source_new(context)
    return all(
        await collect(
            vulns_domain.remove_vulnerability(
                context.loaders,
                finding_id,
                vuln.id,
                justification,
                user_email,
                source,
                include_closed_vuln=True,
            )
            for vuln in vulnerabilities
        )
    )


async def get_closed_vulnerabilities(
    loaders: Any,
    finding_id: str,
) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    return len(vulns_utils.filter_closed_vulns(vulns))


async def get_finding_open_age(loaders: Any, finding_id: str) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns_new(vulns)
    vulns_historic_loader: DataLoader = loaders.vulnerability_historic_state
    vulns_historic_state: Tuple[
        Tuple[VulnerabilityState, ...]
    ] = await vulns_historic_loader.load_many([vuln.id for vuln in open_vulns])
    report_dates = vulns_utils.get_report_dates(vulns_historic_state)
    if report_dates:
        oldest_report_date = min(report_dates)
        return (datetime_utils.get_now() - oldest_report_date).days
    return 0


async def get_last_closed_vulnerability_info(
    loaders: Any,
    findings: Tuple[Finding, ...],
) -> Tuple[Decimal, Optional[Vulnerability]]:
    """Get days since the last closed vulnerability."""
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    valid_findings_ids = [
        finding.id for finding in findings if not is_deleted(finding)
    ]
    vulns: Tuple[
        Vulnerability, ...
    ] = await finding_vulns_loader.load_many_chained(valid_findings_ids)
    closed_vulns = vulns_utils.filter_closed_vulns(vulns)
    closing_vuln_dates = [
        vulns_utils.get_closing_date(vuln) for vuln in closed_vulns
    ]
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i) for i, v in enumerate(closing_vuln_dates)
        )
        last_closed_vuln: Vulnerability = closed_vulns[date_index]
        current_date = max(closing_vuln_dates)
        last_closed_days = Decimal(
            (datetime_utils.get_now().date() - current_date).days
        ).quantize(Decimal("0.1"))
    else:
        last_closed_days = Decimal(0)
        last_closed_vuln = None
    return last_closed_days, last_closed_vuln


async def get_is_verified(loaders: Any, finding_id: str) -> bool:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns_new(vulns)
    remediated_vulns = vulns_utils.filter_remediated(open_vulns)
    return len(remediated_vulns) == 0


async def get_max_open_severity(
    loaders: Any, findings: Tuple[Finding, ...]
) -> Tuple[Decimal, Optional[Finding]]:
    open_vulns = await collect(
        get_open_vulnerabilities(loaders, finding.id) for finding in findings
    )
    open_findings = [
        finding
        for finding, open_vulns_count in zip(findings, open_vulns)
        if open_vulns_count > 0
    ]
    total_severity: List[float] = [
        float(get_severity_score(finding.severity))
        for finding in open_findings
    ]
    if total_severity:
        severity, severity_index = max(
            (v, i) for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal("0.1"))
        max_severity_finding = open_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal("0.1"))
        max_severity_finding = None
    return max_severity, max_severity_finding


async def get_newest_vulnerability_report_date(
    loaders: Any, finding_id: str
) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    vulns_historic_loader: DataLoader = loaders.vulnerability_historic_state
    vulns_historic_state: Tuple[
        Tuple[VulnerabilityState, ...]
    ] = await vulns_historic_loader.load_many([vuln.id for vuln in vulns])
    report_dates = vulns_utils.get_report_dates(vulns_historic_state)
    if report_dates:
        return datetime_utils.get_as_utc_iso_format(max(report_dates))
    return ""


async def get_open_vulnerabilities(loaders: Any, finding_id: str) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    return len(vulns_utils.filter_open_vulns_new(vulns))


async def _is_pending_verification(
    loaders: Any,
    finding_id: str,
) -> bool:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    finding_vulns = await finding_vulns_loader.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns_new(finding_vulns)
    reattack_requested = vulns_utils.filter_remediated(open_vulns)
    return len(reattack_requested) > 0


async def get_pending_verification_findings(
    loaders: Any,
    group_name: str,
) -> Tuple[Finding, ...]:
    """Gets findings pending for verification."""
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    are_pending_verifications = await collect(
        _is_pending_verification(loaders, finding.id) for finding in findings
    )
    return tuple(
        finding
        for finding, is_pending_verification in zip(
            findings, are_pending_verifications
        )
        if is_pending_verification
    )


def get_report_days(report_date: str) -> int:
    """Gets amount of days from a report date."""
    days = 0
    if report_date:
        date = datetime.fromisoformat(report_date)
        days = (datetime_utils.get_now() - date).days
    return days


def get_severity_score(
    severity: Union[Finding20Severity, Finding31Severity]
) -> Decimal:
    if isinstance(severity, Finding31Severity):
        base_score = cvss_new.get_cvss3_basescore(severity)
        return cvss_new.get_cvss3_temporal(severity, base_score)

    base_score = cvss_new.get_cvss2_basescore(severity)
    return cvss_new.get_cvss2_temporal(severity, base_score)


async def get_status(loaders: Any, finding_id: str) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns: Tuple[Vulnerability, ...] = vulns_utils.filter_open_vulns_new(
        vulns
    )
    return "open" if open_vulns else "closed"


async def get_total_treatment(
    loaders: Any,
    findings: Tuple[Finding, ...],
) -> Dict[str, int]:
    """Get the total vulnerability treatment of all the findings."""
    finding_vulns_loader = loaders.finding_vulns_nzr_typed
    non_deleted_findings = tuple(
        finding for finding in findings if not is_deleted(finding)
    )
    vulns: Tuple[
        Vulnerability, ...
    ] = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in non_deleted_findings]
    )
    treatment_counter = Counter(
        vuln.treatment.status
        for vuln in vulns
        if vuln.treatment
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    return {
        "accepted": treatment_counter[VulnerabilityTreatmentStatus.ACCEPTED],
        "acceptedUndefined": treatment_counter[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        "inProgress": treatment_counter[
            VulnerabilityTreatmentStatus.IN_PROGRESS
        ],
        "undefined": treatment_counter[VulnerabilityTreatmentStatus.NEW],
    }


@newrelic.agent.function_trace()
def get_tracking_vulnerabilities(
    vulns_state: Tuple[Tuple[VulnerabilityState, ...], ...],
    vulns_treatment: Tuple[Tuple[VulnerabilityTreatment, ...], ...],
) -> List[TrackingItem]:
    """Get tracking vulnerabilities dictionary."""
    states_actions = vulns_utils.get_state_actions(vulns_state)
    treatments_actions = vulns_utils.get_treatment_actions(vulns_treatment)
    tracking_actions = list(
        sorted(
            states_actions + treatments_actions,
            key=lambda action: datetime_utils.get_from_str(
                action.date, "%Y-%m-%d"
            ),
        )
    )
    return [
        TrackingItem(
            cycle=index,
            open=action.times if action.action == "OPEN" else 0,
            closed=action.times if action.action == "CLOSED" else 0,
            date=action.date,
            accepted=action.times if action.action == "ACCEPTED" else 0,
            accepted_undefined=(
                action.times if action.action == "ACCEPTED_UNDEFINED" else 0
            ),
            manager=action.manager,
            justification=action.justification,
        )
        for index, action in enumerate(tracking_actions)
    ]


async def get_treatment_summary(
    loaders: Any,
    finding_id: str,
) -> Treatments:
    finding_vulns_loader = loaders.finding_vulns_nzr_typed
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    open_vulnerabilities = vulns_utils.filter_open_vulns_new(vulnerabilities)
    return vulns_domain.get_treatments_count(open_vulnerabilities)


async def _get_wheres(
    loaders: Any, finding_id: str, limit: Optional[int] = None
) -> List[str]:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    finding_vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns_new(finding_vulns)
    wheres: List[str] = sorted(set(vuln.where for vuln in open_vulns))
    if limit:
        wheres = wheres[:limit]
    return wheres


async def get_where(loaders: Any, finding_id: str) -> str:
    """
    General locations of the Vulnerabilities. It is limited to 20 locations.
    """
    return ", ".join(await _get_wheres(loaders, finding_id, limit=20))


async def has_access_to_finding(
    loaders: Any, email: str, finding_id: str
) -> bool:
    """Verify if the user has access to a finding submission."""
    finding: Finding = await loaders.finding.load(finding_id)
    has_access = await authz.has_access_to_group(email, finding.group_name)
    return has_access


def is_deleted(finding: Finding) -> bool:
    return finding.state.status == FindingStateStatus.DELETED


async def mask_finding(  # pylint: disable=too-many-locals
    loaders: Any, finding: Finding
) -> bool:
    mask_finding_coroutines = []
    mask_new_finding_coroutines = []
    new_evidences = finding.evidences._replace(
        **{
            evidence_name: evidence._replace(description=MASKED, url=MASKED)
            for evidence_name in finding.evidences._fields
            for evidence in [getattr(finding.evidences, evidence_name)]
            if evidence
        }
    )
    metadata = FindingMetadataToUpdate(
        affected_systems=MASKED,
        attack_vector_description=MASKED,
        description=MASKED,
        evidences=new_evidences,
        recommendation=MASKED,
        threat=MASKED,
    )
    mask_new_finding_coroutines.append(
        findings_model.update_metadata(
            group_name=finding.group_name,
            finding_id=finding.id,
            metadata=metadata,
            is_removed=finding.state.status == FindingStateStatus.DELETED,
        )
    )
    finding_historic_verification_loader = (
        loaders.finding_historic_verification
    )
    finding_historic_verification: Tuple[
        FindingVerification, ...
    ] = await finding_historic_verification_loader.load(finding.id)
    new_historic_verification = tuple(
        verification._replace(
            status=FindingVerificationStatus.MASKED, modified_by=MASKED
        )
        for verification in finding_historic_verification
    )
    mask_new_finding_coroutines.append(
        findings_model.update_historic_verification(
            group_name=finding.group_name,
            finding_id=finding.id,
            historic_verification=new_historic_verification,
            is_removed=finding.state.status == FindingStateStatus.DELETED,
        )
    )
    list_evidences_files = await findings_storage.search_evidence(
        f"{finding.group_name}/{finding.id}"
    )
    evidence_s3_coroutines = [
        findings_storage.remove_evidence(file_name)
        for file_name in list_evidences_files
    ]
    mask_new_finding_coroutines.extend(evidence_s3_coroutines)
    comments_and_observations = await comments_domain.get(
        "comment", finding.id
    ) + await comments_domain.get("observation", finding.id)
    comments_coroutines = [
        comments_domain.delete(comment["comment_id"], finding.id)
        for comment in comments_and_observations
    ]
    mask_finding_coroutines.extend(comments_coroutines)
    finding_all_vulns_loader = loaders.finding_vulns_all_typed
    vulns: Tuple[Vulnerability, ...] = await finding_all_vulns_loader.load(
        finding.id
    )
    mask_vulns_coroutines = [
        vulns_domain.mask_vulnerability(
            loaders=loaders,
            finding_id=finding.id,
            vulnerability_id=vuln.id,
        )
        for vuln in vulns
    ]
    mask_finding_coroutines.extend(mask_vulns_coroutines)
    await collect(mask_new_finding_coroutines)
    return all(await collect(mask_finding_coroutines))


async def request_vulnerabilities_verification(
    loaders: Any,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vulnerability_ids: Set[str],
) -> None:
    finding_loader = loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids_new(
        loaders,
        finding_id,
        vulnerability_ids,
    )
    vulnerabilities = [
        vulns_utils.validate_requested_verification(vuln)
        for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    user_email: str = user_info["user_email"]
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        status=FindingVerificationStatus.REQUESTED,
        vulnerability_ids=vulnerability_ids,
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    comment_data = {
        "comment_type": "verification",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    await comments_domain.add(finding_id, comment_data, user_info)
    success = all(
        await collect(map(vulns_domain.request_verification, vulnerabilities))
    )
    if not success:
        LOGGER.error("An error occurred remediating", **NOEXTRA)
        raise NotVerificationRequested()

    schedule(
        findings_mail.send_mail_remediate_finding(
            loaders,
            user_email,
            finding.id,
            finding.title,
            finding.group_name,
            justification,
        )
    )


async def update_description(
    loaders: Any, finding_id: str, description: FindingDescriptionToUpdate
) -> None:
    validations.validate_fields(
        list(filter(None, description._asdict().values()))
    )
    findings_utils.is_valid_finding_title(description.title)

    finding_loader = loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    metadata = FindingMetadataToUpdate(
        affected_systems=description.affected_systems,
        attack_vector_description=description.attack_vector_description,
        description=description.description,
        recommendation=description.recommendation,
        sorts=description.sorts,
        threat=description.threat,
        title=description.title,
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def update_severity(
    loaders: Any,
    finding_id: str,
    severity: Union[Finding20Severity, Finding31Severity],
) -> None:
    finding_loader = loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    if isinstance(severity, Finding31Severity):
        privileges = cvss_new.calculate_privileges(
            float(severity.privileges_required),
            float(severity.severity_scope),
        )
        privileges_required = Decimal(privileges).quantize(Decimal("0.01"))
        modified_privileges = cvss_new.calculate_privileges(
            float(severity.modified_privileges_required),
            float(severity.modified_severity_scope),
        )
        modified_privileges_required = Decimal(modified_privileges).quantize(
            Decimal("0.01")
        )
        updated_severity = severity._replace(
            privileges_required=privileges_required,
            modified_privileges_required=modified_privileges_required,
        )
    else:
        updated_severity = severity

    metadata = FindingMetadataToUpdate(severity=updated_severity)
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def verify_vulnerabilities(  # pylint: disable=too-many-locals
    *,
    context: Any,
    finding_id: str,
    user_info: UserType,
    justification: str,
    open_vulns_ids: List[str],
    closed_vulns_ids: List[str],
    vulns_to_close_from_file: List[Vulnerability],
) -> bool:
    # All vulns must be open before verifying them
    # we will just keep them open or close them
    # in either case, their historic_verification is updated to VERIFIED
    finding_loader = context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    if not operation_can_be_executed(context, finding.title):
        raise MachineCanNotOperate()

    finding_vulns_loader = context.loaders.finding_vulns_all_typed
    vulnerability_ids: List[str] = open_vulns_ids + closed_vulns_ids
    vulnerabilities = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln.id in vulnerability_ids
    ]
    vulnerabilities = [
        vulns_utils.validate_reattack_requested(vuln)
        for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_iso_date()
    user_email: str = user_info["user_email"]

    # Modify the verification state to mark the finding as verified
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=user_email,
        modified_date=today,
        status=FindingVerificationStatus.VERIFIED,
        vulnerability_ids=set(vulnerability_ids),
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    comment_data = {
        "comment_type": "verification",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    await comments_domain.add(finding_id, comment_data, user_info)

    # Modify the verification state to mark all passed vulns as verified
    success = all(
        await collect(map(vulns_domain.verify_vulnerability, vulnerabilities))
    )
    if success:
        # Open vulns that remain open are not modified in the DB
        # Open vulns that were closed must be persisted to the DB as closed
        success = await vulns_domain.verify(
            context=context,
            vulnerabilities=vulnerabilities,
            modified_date=today,
            closed_vulns_ids=closed_vulns_ids,
            vulns_to_close_from_file=vulns_to_close_from_file,
        )
    else:
        LOGGER.error("An error occurred verifying", **NOEXTRA)
    return success


async def get_oldest_no_treatment(
    loaders: Any,
    findings: Tuple[Finding, ...],
) -> Optional[Dict[str, str]]:
    """Get the finding with oldest "no treatment" vulnerability."""
    finding_vulns_loader = loaders.finding_vulns_nzr_typed
    vulns = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in findings]
    )
    open_vulns = vulns_utils.filter_open_vulns_new(vulns)
    no_treatment_vulns = vulns_utils.filter_no_treatment_vulns(open_vulns)

    if not no_treatment_vulns:
        return None

    treatment_dates: List[datetime] = [
        datetime.fromisoformat(vuln.treatment.modified_date)
        for vuln in no_treatment_vulns
    ]
    vulns_info = [
        (
            date,
            vuln.finding_id,
        )
        for vuln, date in zip(no_treatment_vulns, treatment_dates)
    ]
    oldest_date, oldest_finding_id = min(vulns_info)
    oldest_finding: Finding = next(
        finding for finding in findings if finding.id == oldest_finding_id
    )
    return {
        "oldest_name": oldest_finding.title,
        "oldest_age": (datetime_utils.get_now() - oldest_date).days,
    }


async def get_oldest_open_vulnerability_report_date(
    loaders: Any,
    finding_id: str,
) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns_new(vulns)
    vulns_historic_loader: DataLoader = loaders.vulnerability_historic_state
    vulns_historic_state: Tuple[
        Tuple[VulnerabilityState, ...]
    ] = await vulns_historic_loader.load_many([vuln.id for vuln in open_vulns])
    report_dates = vulns_utils.get_report_dates(vulns_historic_state)
    if report_dates:
        return datetime_utils.get_as_utc_iso_format(min(report_dates))
    return ""


async def get_oldest_vulnerability_report_date(
    loaders: Any,
    finding_id: str,
) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr_typed
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    vulns_historic_loader: DataLoader = loaders.vulnerability_historic_state
    vulns_historic_state: Tuple[
        Tuple[VulnerabilityState, ...]
    ] = await vulns_historic_loader.load_many([vuln.id for vuln in vulns])
    report_dates = vulns_utils.get_report_dates(vulns_historic_state)
    if report_dates:
        return datetime_utils.get_as_utc_iso_format(min(report_dates))
    return ""
