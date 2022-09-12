# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_ENVIRONMENT,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidCommentParent,
    MachineCanNotOperate,
    NotVerificationRequested,
    PermissionDenied,
    VulnNotFound,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
)
from db_model.enums import (
    StateRemovalJustification,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
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
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from finding_comments import (
    domain as comments_domain,
)
from findings import (
    storage as findings_storage,
)
from findings.types import (
    FindingDescriptionToUpdate,
    Tracking,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from machine.availability import (
    operation_can_be_executed,
)
from machine.jobs import (
    get_finding_code_from_title,
    queue_job_new,
)
from mailer import (
    findings as findings_mail,
)
from newutils import (
    cvss as cvss_utils,
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from redshift import (
    findings as redshift_findings,
)
from settings import (
    LOGGING,
)
from time import (
    time,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from vulnerabilities import (
    domain as vulns_domain,
)
from vulnerabilities.types import (
    Treatments,
    Verifications,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _send_to_redshift(
    *,
    loaders: Any,
    finding: Finding,
) -> None:
    historic_state = await loaders.finding_historic_state.load(finding.id)
    historic_verification = await loaders.finding_historic_verification.load(
        finding.id
    )
    await redshift_findings.insert_finding(
        finding=finding,
        historic_state=historic_state,
        historic_verification=historic_verification,
    )
    LOGGER.info(
        "Finding stored in redshift",
        extra={
            "extra": {
                "finding_id": finding.id,
                "group_name": finding.group_name,
            }
        },
    )


async def add_comment(
    info: GraphQLResolveInfo,
    user_email: str,
    comment_data: FindingComment,
    finding_id: str,
    group_name: str,
) -> None:
    loaders = info.context.loaders
    param_type = comment_data.comment_type
    parent_comment = (
        str(comment_data.parent_id) if comment_data.parent_id else "0"
    )
    content = comment_data.content
    validations.validate_field_length(content, 20000)
    await authz.validate_handle_comment_scope(
        loaders, content, user_email, group_name, parent_comment
    )
    if param_type == CommentType.OBSERVATION:
        enforcer = await authz.get_group_level_enforcer(loaders, user_email)
        if not enforcer(group_name, "post_finding_observation"):
            raise PermissionDenied()
    if parent_comment != "0":
        finding_comments = [
            comment.id
            for comment in await loaders.finding_comments.load(
                (comment_data.comment_type, finding_id)
            )
        ]
        if parent_comment not in finding_comments:
            raise InvalidCommentParent()
    await comments_domain.add(comment_data)


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
    if (
        not user_email.endswith("@fluidattacks.com")
        and finding.state.status == FindingStateStatus.APPROVED
    ):
        await _send_to_redshift(
            loaders=context.loaders,
            finding=finding,
        )
    await findings_model.remove(
        group_name=finding.group_name, finding_id=finding.id
    )


async def remove_vulnerabilities(
    context: Any,
    finding_id: str,
    justification: StateRemovalJustification,
    user_email: str,
) -> None:
    finding_vulns_loader = context.loaders.finding_vulnerabilities
    vulnerabilities: Tuple[Vulnerability] = await finding_vulns_loader.load(
        finding_id
    )
    source = requests_utils.get_source_new(context)
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


async def get_closed_vulnerabilities(
    loaders: Any,
    finding_id: str,
) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    return len(vulns_utils.filter_closed_vulns(vulns))


async def get_finding_open_age(loaders: Any, finding_id: str) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        return (datetime_utils.get_now() - oldest_report_date).days
    return 0


async def get_last_closed_vulnerability_info(
    loaders: Any,
    findings: tuple[Finding, ...],
) -> tuple[int, Optional[Vulnerability]]:
    """Get days since the last closed vulnerability and its metadata."""
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    valid_findings_ids = [
        finding.id for finding in findings if not is_deleted(finding)
    ]
    vulns: tuple[
        Vulnerability, ...
    ] = await finding_vulns_loader.load_many_chained(valid_findings_ids)
    closed_vulns = vulns_utils.filter_closed_vulns(vulns)
    closing_vuln_dates = [
        vulns_utils.get_closing_date(vuln) for vuln in closed_vulns
    ]
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i) for i, v in enumerate(closing_vuln_dates) if v is not None
        )
        last_closed_vuln: Optional[Vulnerability] = closed_vulns[date_index]
        last_closed_days = (
            datetime_utils.get_now().date() - current_date
        ).days
    else:
        last_closed_days = 0
        last_closed_vuln = None
    return last_closed_days, last_closed_vuln


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
        max_severity_finding: Optional[Finding] = open_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal("0.1"))
        max_severity_finding = None
    return max_severity, max_severity_finding


async def get_newest_vulnerability_report_date(
    loaders: Any,
    finding_id: str,
) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    report_dates = vulns_utils.get_report_dates(vulns)
    newest_report_date: str = (
        datetime_utils.get_as_utc_iso_format(max(report_dates))
        if report_dates
        else ""
    )
    return newest_report_date


async def get_open_vulnerabilities(loaders: Any, finding_id: str) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    return len(vulns_utils.filter_open_vulns(vulns))


async def _is_pending_verification(loaders: Any, finding_id: str) -> bool:
    return len(await get_vulnerabilities_to_reattack(loaders, finding_id)) > 0


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


def get_severity_level(severity: Decimal) -> str:
    if severity <= 3.9:
        return "low"
    if 4 <= severity <= 6.9:
        return "medium"
    if 7 <= severity <= 8.9:
        return "high"

    return "critical"


def get_severity_score(
    severity: Union[Finding20Severity, Finding31Severity]
) -> Decimal:
    if isinstance(severity, Finding31Severity):
        base_score = cvss_utils.get_cvss3_basescore(severity)
        return cvss_utils.get_cvss3_temporal(severity, base_score)

    base_score = cvss_utils.get_cvss2_basescore(severity)
    return cvss_utils.get_cvss2_temporal(severity, base_score)


async def get_status(loaders: Any, finding_id: str) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns: Tuple[Vulnerability, ...] = vulns_utils.filter_open_vulns(
        vulns
    )
    return "open" if open_vulns else "closed"


def get_tracking_vulnerabilities(
    vulns_state: Tuple[Tuple[VulnerabilityState, ...], ...],
    vulns_treatment: Tuple[Tuple[VulnerabilityTreatment, ...], ...],
) -> List[Tracking]:
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
        Tracking(
            cycle=index,
            open=action.times if action.action == "OPEN" else 0,
            closed=action.times if action.action == "CLOSED" else 0,
            date=action.date,
            accepted=action.times if action.action == "ACCEPTED" else 0,
            accepted_undefined=(
                action.times if action.action == "ACCEPTED_UNDEFINED" else 0
            ),
            assigned=action.assigned,
            justification=action.justification,
        )
        for index, action in enumerate(tracking_actions)
    ]


async def get_treatment_summary(
    loaders: Any,
    finding_id: str,
) -> Treatments:
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    open_vulnerabilities = vulns_utils.filter_open_vulns(vulnerabilities)
    return vulns_domain.get_treatments_count(open_vulnerabilities)


async def get_verification_summary(
    loaders: Any,
    finding_id: str,
) -> Verifications:
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    return vulns_domain.get_verifications_count(vulnerabilities)


async def _get_wheres(
    loaders: Any, finding_id: str, limit: Optional[int] = None
) -> List[str]:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    finding_vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns(finding_vulns)
    wheres: List[str] = list(set(vuln.where for vuln in open_vulns))
    if limit:
        wheres = wheres[:limit]
    return wheres


async def get_where(loaders: Any, finding_id: str) -> str:
    """
    General locations of the Vulnerabilities. It is limited to 20 locations.
    """
    return ", ".join(sorted(await _get_wheres(loaders, finding_id, limit=20)))


async def has_access_to_finding(
    loaders: Any, email: str, finding_id: str
) -> bool:
    """Verify if the user has access to a finding submission."""
    finding: Finding = await loaders.finding.load(finding_id)
    return await authz.has_access_to_group(loaders, email, finding.group_name)


def is_deleted(finding: Finding) -> bool:
    return finding.state.status == FindingStateStatus.DELETED


async def mask_finding(loaders: Any, finding: Finding) -> None:
    comments_and_observations: list[
        FindingComment
    ] = await loaders.finding_comments.load(
        (CommentType.COMMENT, finding.id)
    ) + await loaders.finding_comments.load(
        (CommentType.OBSERVATION, finding.id)
    )
    await collect(
        comments_domain.remove(comment.id, finding.id)
        for comment in comments_and_observations
    )
    list_evidences_files = await findings_storage.search_evidence(
        f"{finding.group_name}/{finding.id}"
    )
    await collect(
        findings_storage.remove_evidence(file_name)
        for file_name in list_evidences_files
    )

    finding_all_vulns_loader = loaders.finding_vulnerabilities_all
    vulns: Tuple[Vulnerability, ...] = await finding_all_vulns_loader.load(
        finding.id
    )
    await collect(
        tuple(
            vulns_domain.mask_vulnerability(
                loaders=loaders,
                finding_id=finding.id,
                vulnerability=vuln,
            )
            for vuln in vulns
        ),
        workers=4,
    )

    if (
        finding.state.status != FindingStateStatus.DELETED
        or not finding.state.modified_by.endswith("@fluidattacks.com")
    ):
        await _send_to_redshift(loaders=loaders, finding=finding)

    await findings_model.remove(
        group_name=finding.group_name, finding_id=finding.id
    )
    LOGGER.info(
        "Finding masked",
        extra={
            "extra": {
                "finding_id": finding.id,
                "group_name": finding.group_name,
            }
        },
    )


async def request_vulnerabilities_verification(  # noqa pylint: disable=too-many-arguments, too-many-locals
    loaders: Any,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vulnerability_ids: Set[str],
    is_closing_event: bool = False,
) -> None:
    finding: Finding = await loaders.finding.load(finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids(
        loaders,
        finding_id,
        vulnerability_ids,
    )
    vulnerabilities = tuple(
        vulns_utils.validate_requested_verification(vuln, is_closing_event)
        for vuln in vulnerabilities
    )
    vulnerabilities = tuple(
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    )
    if not vulnerabilities:
        raise VulnNotFound()
    root_ids = {
        vuln.root_id
        for vuln in vulnerabilities
        if vuln.root_id and not check_hold(vuln)
    }
    roots: tuple[GitRoot, ...] = await loaders.group_roots.load(
        finding.group_name
    )
    root_nicknames: tuple[str, ...] = tuple(
        root.state.nickname for root in roots if root.id in root_ids
    )
    if root_nicknames and FI_ENVIRONMENT == "production":
        with suppress(ClientError):
            if finding_code := get_finding_code_from_title(finding.title):
                await queue_job_new(
                    group_name=finding.group_name,
                    roots=list(root_nicknames),
                    finding_codes=[
                        finding_code,
                    ],
                    dataloaders=loaders,
                    clone_before=True,
                )
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
    current_time = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_now()
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.VERIFICATION,
        content=justification,
        parent_id="0",
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=current_time,
    )
    await comments_domain.add(comment_data)
    success = all(
        await collect(map(vulns_domain.request_verification, vulnerabilities))
    )
    if not success:
        LOGGER.error("An error occurred remediating")
        raise NotVerificationRequested()

    if any(not check_hold(vuln) for vuln in vulnerabilities):
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


async def send_closed_vulnerabilities_report(
    *,
    loaders: Any,
    finding_id: str,
    closed_vulnerabilities_id: List[str],
) -> None:
    finding: Finding = await loaders.finding.load(finding_id)
    finding_vulns_loader = loaders.finding_vulnerabilities_all
    finding_vulns_loader.clear(finding_id)
    severity_score: Decimal = get_severity_score(finding.severity)
    closed_vulnerabilities: List[Vulnerability] = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln.id in closed_vulnerabilities_id
    ]

    exposure: Decimal = 4 ** (severity_score - 4)
    vulns_closed_props: dict[str, Any] = {}

    for vuln in closed_vulnerabilities:
        report_date = datetime_utils.get_date_from_iso_str(
            vuln.unreliable_indicators.unreliable_report_date
        )
        days_open = (datetime_utils.get_now().date() - report_date).days
        reattack_requester = (
            vuln.unreliable_indicators.unreliable_last_reattack_requester
        )
        vulns_closed_props[vuln.id] = {
            "Location": vuln.where,
            "Assigned": vuln.treatment.assigned if vuln.treatment else None,
            "Report date": report_date,
            "Time to remediate": f"{days_open} calendar days",
            "Reattack requester": reattack_requester,
            "Reduction in exposure": round(exposure, 1),
        }

    schedule(
        send_vulnerability_report(
            loaders=loaders,
            finding_id=finding_id,
            vulnerabilities_properties=vulns_closed_props,
            is_closed=True,
        )
    )


async def send_vulnerability_report(
    *,
    loaders: Any,
    finding_id: str,
    vulnerabilities_properties: Dict[str, Any],
    is_closed: bool = False,
) -> None:
    finding: Finding = await loaders.finding.load(finding_id)
    severity_score: Decimal = get_severity_score(finding.severity)
    severity_level: str = get_severity_level(severity_score)
    if (
        severity_score >= 7.0
        and finding.state.status == FindingStateStatus.APPROVED
    ):
        schedule(
            findings_mail.send_mail_vulnerability_report(
                loaders=loaders,
                group_name=finding.group_name,
                finding_title=finding.title,
                finding_id=finding_id,
                vulnerabilities_properties=vulnerabilities_properties,
                severity_score=severity_score,
                severity_level=severity_level,
                is_closed=is_closed,
            )
        )


async def update_description(
    loaders: Any, finding_id: str, description: FindingDescriptionToUpdate
) -> None:
    validations.validate_fields(
        list(filter(None, description._asdict().values()))
    )
    if description.title:
        await findings_utils.is_valid_finding_title(description.title)

    finding_loader = loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    metadata = FindingMetadataToUpdate(
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
    updated_severity: Union[Finding20Severity, Finding31Severity]
    if isinstance(severity, Finding31Severity):
        privileges = cvss_utils.calculate_privileges(
            float(severity.privileges_required),
            float(severity.severity_scope),
        )
        privileges_required = Decimal(privileges).quantize(Decimal("0.01"))
        modified_privileges = cvss_utils.calculate_privileges(
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
    context: Optional[Any] = None,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    open_vulns_ids: List[str],
    closed_vulns_ids: List[str],
    vulns_to_close_from_file: List[Vulnerability],
    loaders: Any,
    is_reattack_open: Optional[bool] = None,
    is_closing_event: bool = False,
) -> None:
    # All vulns must be open before verifying them
    # we will just keep them open or close them
    # in either case, their historic_verification is updated to VERIFIED
    finding_loader = loaders.finding
    finding_loader.clear(finding_id)
    finding: Finding = await finding_loader.load(finding_id)
    if context and not operation_can_be_executed(context, finding.title):
        raise MachineCanNotOperate()

    finding_vulns_loader = loaders.finding_vulnerabilities_all
    vulnerability_ids: List[str] = open_vulns_ids + closed_vulns_ids
    vulnerabilities = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln.id in vulnerability_ids
    ]
    # Sometimes vulns on hold end up being closed before the event is solved
    # Therefore, this allows these vulns to be auto-verified when it happens
    if not is_closing_event:
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
    user_email = user_info["user_email"]

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

    current_time = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_now()
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.VERIFICATION,
        content=justification,
        parent_id="0",
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=current_time,
    )
    if is_reattack_open is None:
        await comments_domain.add(comment_data)
    # Modify the verification state to mark all passed vulns as verified
    await collect(map(vulns_domain.verify_vulnerability, vulnerabilities))
    # Open vulns that remain open are not modified in the DB
    # Open vulns that were closed must be persisted to the DB as closed
    await vulns_domain.verify(
        context=context,
        loaders=loaders,
        modified_date=today,
        closed_vulns_ids=closed_vulns_ids,
        vulns_to_close_from_file=vulns_to_close_from_file,
    )
    if closed_vulns_ids:
        schedule(
            send_closed_vulnerabilities_report(
                loaders=loaders,
                finding_id=finding_id,
                closed_vulnerabilities_id=closed_vulns_ids,
            )
        )


async def get_oldest_no_treatment(
    loaders: Any,
    findings: Tuple[Finding, ...],
) -> Optional[Dict[str, Union[int, str]]]:
    """Get the finding with oldest "no treatment" vulnerability."""
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    vulns = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in findings]
    )
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    no_treatment_vulns = vulns_utils.filter_no_treatment_vulns(open_vulns)
    if not no_treatment_vulns:
        return None
    treatment_dates: List[datetime] = [
        datetime.fromisoformat(vuln.treatment.modified_date)
        for vuln in no_treatment_vulns
        if vuln.treatment
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
        "oldest_name": str(oldest_finding.title),
        "oldest_age": int((datetime_utils.get_now() - oldest_date).days),
    }


async def get_oldest_open_vulnerability_report_date(
    loaders: Any,
    finding_id: str,
) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)
    oldest_open_report_date: str = (
        datetime_utils.get_as_utc_iso_format(min(report_dates))
        if report_dates
        else ""
    )
    return oldest_open_report_date


async def get_oldest_vulnerability_report_date(
    loaders: Any,
    finding_id: str,
) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulnerabilities_nzr
    vulns: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        finding_id
    )
    report_dates = vulns_utils.get_report_dates(vulns)
    oldest_report_date: str = (
        datetime_utils.get_as_utc_iso_format(min(report_dates))
        if report_dates
        else ""
    )
    return oldest_report_date


async def get_vulnerabilities_to_reattack(
    loaders: Any,
    finding_id: str,
) -> Tuple[Vulnerability, ...]:
    finding_vulns = await loaders.finding_vulnerabilities_nzr.load(finding_id)
    return vulns_utils.filter_open_vulns(
        vulns_utils.filter_remediated(finding_vulns)
    )


def check_hold(vuln: Vulnerability) -> bool:
    return (
        vuln.verification is not None
        and vuln.verification.status == VulnerabilityVerificationStatus.ON_HOLD
    )
