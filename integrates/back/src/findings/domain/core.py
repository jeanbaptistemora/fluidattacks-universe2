# pylint: disable=too-many-lines
from aioextensions import (
    collect,
    schedule,
)
import authz
from botocore.exceptions import (
    ClientError,
)
from collections.abc import (
    Iterable,
)
from context import (
    FI_ENVIRONMENT,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    FindingNotFound,
    InvalidCommentParent,
    InvalidVulnerabilityRequirement,
    MachineCanNotOperate,
    PermissionDenied,
    RepeatedFindingDescription,
    RepeatedFindingMachineDescription,
    RepeatedFindingSeverity,
    RepeatedFindingThreat,
    RequiredUnfulfilledRequirements,
    RootNotFound,
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
    timezone,
)
from db_model import (
    findings as findings_model,
)
from db_model.enums import (
    Source,
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
    SeverityScore,
)
from db_model.roots.types import (
    GitRootState,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
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
    FindingAttributesToAdd,
    FindingDescriptionToUpdate,
    Tracking,
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
    machine as machine_utils,
    validations,
    vulnerabilities as vulns_utils,
)
import pytz
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
from settings.various import (
    TIME_ZONE,
)
from time import (
    time,
)
from typing import (
    Any,
    TypedDict,
)
import uuid
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


class VulnsProperties(TypedDict):
    remaining_exposure: int
    severity_level: str
    severity_score: Decimal
    vulns_props: dict[str, dict[str, dict[str, Any]]]


async def _validate_finding_requirements(
    loaders: Dataloaders, title: str, unfulfilled_requirements: list[str]
) -> None:
    if not unfulfilled_requirements:
        raise RequiredUnfulfilledRequirements()
    vulnerabilities_file = await loaders.vulnerabilities_file.load("")
    criteria_vulnerability_id = title.split(".")[0].strip()
    criteria_vulnerability = vulnerabilities_file[criteria_vulnerability_id]
    criteria_vulnerabilily_requirements: list[str] = (
        criteria_vulnerability["requirements"]
        if criteria_vulnerability
        else []
    )
    if not set(unfulfilled_requirements).issubset(
        criteria_vulnerabilily_requirements
    ):
        raise InvalidVulnerabilityRequirement()


async def _validate_duplicated_finding(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    title: str,
    description: str,
    threat: str,
    severity: Finding20Severity | Finding31Severity,
    current_finding: Finding | None = None,
) -> None:
    group = await loaders.group.load(group_name)
    group_findings = await loaders.group_drafts_and_findings.load(group_name)
    same_type_of_findings = (
        [
            finding
            for finding in group_findings
            if finding.id != current_finding.id
            and (
                finding.title.split(".")[0].strip()
                == title.split(".")[0].strip()
            )
        ]
        if current_finding
        else [
            finding
            for finding in group_findings
            if finding.title.split(".")[0].strip()
            == title.split(".")[0].strip()
        ]
    )
    for finding in same_type_of_findings:
        if finding.description.strip() == description.strip() and not (
            current_finding is not None
            and current_finding.description.split() == description.split()
        ):
            raise RepeatedFindingDescription()
        if finding.threat.strip() == threat.strip():
            raise RepeatedFindingThreat()
        if finding.severity == severity:
            raise RepeatedFindingSeverity()

    criteria_vulnerabilities = await loaders.vulnerabilities_file.load("")
    criteria_vulnerability: dict[str, Any] = criteria_vulnerabilities[
        title.split(".")[0].strip()
    ]
    duplicated_findings = [
        finding
        for finding in same_type_of_findings
        if machine_utils.has_machine_description(
            finding._replace(
                description=description, threat=threat, severity=severity
            ),
            criteria_vulnerability,
            str(group.language.value).lower(),
        )
    ]
    if duplicated_findings:
        raise RepeatedFindingMachineDescription()


@validations.validate_fields_deco(
    [
        "attributes.attack_vector_description",
        "attributes.description",
        "attributes.recommendation",
        "attributes.unfulfilled_requirements",
        "attributes.threat",
    ]
)
@validations.validate_fields_length_deco(
    [
        "attributes.attack_vector_description",
        "attributes.description",
        "attributes.recommendation",
        "attributes.unfulfilled_requirements",
        "attributes.threat",
    ],
    limit=5000,
)
@validations.validate_fields_length_deco(
    [
        "attributes.attack_vector_description",
        "attributes.description",
        "attributes.recommendation",
        "attributes.unfulfilled_requirements",
        "attributes.threat",
    ],
    limit=0,
    is_greater_than_limit=True,
)
@validations.validate_update_severity_values_deco("attributes.severity")
async def add_finding(
    *,
    loaders: Dataloaders,
    group_name: str,
    stakeholder_email: str,
    attributes: FindingAttributesToAdd,
) -> Finding:
    await findings_utils.is_valid_finding_title(loaders, attributes.title)
    await _validate_finding_requirements(
        loaders, attributes.title, attributes.unfulfilled_requirements
    )
    await _validate_duplicated_finding(
        loaders,
        group_name,
        attributes.title,
        attributes.description,
        attributes.threat,
        attributes.severity,
    )

    finding = Finding(
        hacker_email=stakeholder_email,
        attack_vector_description=attributes.attack_vector_description,
        description=attributes.description,
        group_name=group_name,
        id=str(uuid.uuid4()),
        min_time_to_remediate=attributes.min_time_to_remediate,
        state=FindingState(
            modified_by=stakeholder_email,
            modified_date=datetime_utils.get_utc_now(),
            source=attributes.source,
            status=FindingStateStatus.CREATED,
        ),
        recommendation=attributes.recommendation,
        severity=attributes.severity,
        severity_score=SeverityScore(
            base_score=cvss_utils.get_severity_base_score(attributes.severity),
            temporal_score=cvss_utils.get_severity_temporal_score(
                attributes.severity
            ),
            cvssf=cvss_utils.get_cvssf_score(
                cvss_utils.get_severity_temporal_score(attributes.severity)
            ),
        ),
        title=attributes.title,
        threat=attributes.threat,
        unfulfilled_requirements=sorted(
            set(attributes.unfulfilled_requirements)
        ),
    )
    await findings_model.add(finding=finding)
    return finding


async def get_finding(loaders: Dataloaders, finding_id: str) -> Finding:
    finding = await loaders.finding.load(finding_id)
    if finding is None:
        raise FindingNotFound()

    return finding


@authz.validate_handle_comment_scope_deco(
    "loaders",
    "comment_data.content",
    "user_email",
    "group_name",
    "comment_data.parent_id",
)
@validations.validate_field_length_deco("content", limit=20000)
async def add_comment(
    loaders: Dataloaders,
    user_email: str,
    comment_data: FindingComment,
    finding_id: str,
    group_name: str,
) -> None:
    param_type = comment_data.comment_type
    parent_comment = (
        str(comment_data.parent_id) if comment_data.parent_id else "0"
    )
    if param_type == CommentType.OBSERVATION:
        enforcer = await authz.get_group_level_enforcer(loaders, user_email)
        if not enforcer(group_name, "post_finding_observation"):
            raise PermissionDenied()
    if parent_comment != "0":
        all_finding_comments: list[
            FindingComment
        ] = await comments_domain.get_unformatted_comments(
            loaders=loaders,
            comment_type=comment_data.comment_type,
            finding_id=finding_id,
        )
        finding_comments = {comment.id for comment in all_finding_comments}
        if parent_comment not in finding_comments:
            raise InvalidCommentParent()
    await comments_domain.add(loaders, comment_data, notify=True)


async def remove_all_evidences(finding_id: str, group_name: str) -> None:
    file_names = await findings_storage.search_evidence(
        f"{group_name}/{finding_id}"
    )
    await collect(
        findings_storage.remove_evidence(
            f'{group_name}/{finding_id}/{file_name.split("/")[-1]}'
        )
        for file_name in file_names
    )
    metadata = FindingMetadataToUpdate(evidences=FindingEvidences())
    await findings_model.update_metadata(
        group_name=group_name,
        finding_id=finding_id,
        metadata=metadata,
    )


async def remove_finding(
    loaders: Dataloaders,
    email: str,
    finding_id: str,
    justification: StateRemovalJustification,
    source: Source,
) -> None:
    finding = await get_finding(loaders, finding_id)
    if finding.state.status == FindingStateStatus.DELETED:
        raise FindingNotFound()

    await remove_vulnerabilities(
        loaders,
        finding.id,
        VulnerabilityStateReason[justification.value],
        email,
    )
    await remove_all_evidences(finding.id, finding.group_name)
    await comments_domain.remove_comments(finding_id=finding_id)
    deletion_state = FindingState(
        justification=justification,
        modified_by=email,
        modified_date=datetime_utils.get_utc_now(),
        source=source,
        status=FindingStateStatus.DELETED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=deletion_state,
    )
    if finding.approval is None:
        await findings_model.remove(
            group_name=finding.group_name, finding_id=finding.id
        )


async def remove_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
    justification: VulnerabilityStateReason,
    email: str,
) -> None:
    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    await collect(
        tuple(
            vulns_domain.remove_vulnerability(
                loaders=loaders,
                finding_id=finding_id,
                vulnerability_id=vulnerability.id,
                justification=justification,
                email=email,
                include_closed_vuln=True,
            )
            for vulnerability in vulnerabilities
        ),
        workers=8,
    )


async def get_closed_vulnerabilities(
    loaders: Dataloaders,
    finding_id: str,
) -> int:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    return len(vulns_utils.filter_closed_vulns(vulns))


async def get_finding_open_age(loaders: Dataloaders, finding_id: str) -> int:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        return (datetime_utils.get_now() - oldest_report_date).days
    return 0


async def get_last_closed_vulnerability_info(
    loaders: Dataloaders,
    findings: Iterable[Finding],
) -> tuple[int, Vulnerability | None]:
    """Get days since the last closed vulnerability and its metadata."""
    valid_findings_ids = [
        finding.id for finding in findings if not is_deleted(finding)
    ]
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            valid_findings_ids
        )
    )
    closed_vulns = vulns_utils.filter_closed_vulns(vulns)
    closing_vuln_dates = [
        vulns_utils.get_closing_date(vuln) for vuln in closed_vulns
    ]
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i) for i, v in enumerate(closing_vuln_dates) if v is not None
        )
        last_closed_vuln: Vulnerability | None = closed_vulns[date_index]
        last_closed_days = (
            datetime_utils.get_now().date() - current_date
        ).days
    else:
        last_closed_days = 0
        last_closed_vuln = None
    return last_closed_days, last_closed_vuln


async def get_max_open_severity(
    loaders: Dataloaders, findings: Iterable[Finding]
) -> tuple[Decimal, Finding | None]:
    open_vulns = await collect(
        get_open_vulnerabilities(loaders, finding.id) for finding in findings
    )
    open_findings = [
        finding
        for finding, open_vulns_count in zip(findings, open_vulns)
        if open_vulns_count > 0
    ]
    total_severity: list[float] = [
        float(get_severity_score(finding.severity))
        for finding in open_findings
    ]
    if total_severity:
        severity, severity_index = max(
            (v, i) for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal("0.1"))
        max_severity_finding: Finding | None = open_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal("0.1"))
        max_severity_finding = None
    return max_severity, max_severity_finding


async def get_newest_vulnerability_report_date(
    loaders: Dataloaders,
    finding_id: str,
) -> datetime | None:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    report_dates = vulns_utils.get_report_dates(
        vulns_utils.filter_released_vulns(vulns)
    )

    return max(report_dates) if report_dates else None


async def get_open_vulnerabilities(
    loaders: Dataloaders, finding_id: str
) -> int:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    return len(vulns_utils.filter_open_vulns(vulns))


async def _is_pending_verification(
    loaders: Dataloaders, finding_id: str
) -> bool:
    return len(await get_vulnerabilities_to_reattack(loaders, finding_id)) > 0


async def get_pending_verification_findings(
    loaders: Dataloaders,
    group_name: str,
) -> list[Finding]:
    """Gets findings pending for verification."""
    findings = await loaders.group_findings.load(group_name)
    are_pending_verifications = await collect(
        _is_pending_verification(loaders, finding.id) for finding in findings
    )
    return [
        finding
        for finding, is_pending_verification in zip(
            findings, are_pending_verifications
        )
        if is_pending_verification
    ]


def get_report_days(report_date: datetime | None) -> int:
    """Gets amount of days from a report date."""
    return (
        (datetime_utils.get_utc_now() - report_date).days if report_date else 0
    )


def get_severity_level(severity: Decimal) -> str:
    if severity < 4:
        return "low"
    if 4 <= severity < 7:
        return "medium"
    if 7 <= severity < 9:
        return "high"

    return "critical"


def get_severity_score(
    severity: Finding20Severity | Finding31Severity,
) -> Decimal:
    if isinstance(severity, Finding31Severity):
        base_score = cvss_utils.get_cvss3_basescore(severity)
        return cvss_utils.get_cvss3_temporal(severity, base_score)

    base_score = cvss_utils.get_cvss2_basescore(severity)
    return cvss_utils.get_cvss2_temporal(severity, base_score)


async def get_status(loaders: Dataloaders, finding_id: str) -> str:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    return "VULNERABLE" if open_vulns else "SAFE"


def get_tracking_vulnerabilities(
    vulns_state: Iterable[Iterable[VulnerabilityState]],
    vulns_treatment: Iterable[Iterable[VulnerabilityTreatment]],
) -> list[Tracking]:
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
            open=action.times if action.action == "VULNERABLE" else 0,
            closed=action.times if action.action == "SAFE" else 0,
            date=action.date,
            accepted=action.times if action.action == "ACCEPTED" else 0,
            accepted_undefined=(
                action.times if action.action == "ACCEPTED_UNDEFINED" else 0
            ),
            assigned=action.assigned,
            justification=action.justification,
            safe=action.times if action.action == "SAFE" else 0,
            vulnerable=action.times if action.action == "VULNERABLE" else 0,
        )
        for index, action in enumerate(tracking_actions)
    ]


async def get_treatment_summary(
    loaders: Dataloaders,
    finding_id: str,
) -> Treatments:
    vulnerabilities = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    open_vulnerabilities = vulns_utils.filter_open_vulns(vulnerabilities)
    return vulns_domain.get_treatments_count(open_vulnerabilities)


async def get_verification_summary(
    loaders: Dataloaders,
    finding_id: str,
) -> Verifications:
    vulnerabilities = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    return vulns_domain.get_verifications_count(vulnerabilities)


async def _get_wheres(
    loaders: Dataloaders, finding_id: str, limit: int | None = None
) -> list[str]:
    finding_vulns = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    open_vulns = vulns_utils.filter_open_vulns(finding_vulns)
    wheres: list[str] = list(set(vuln.state.where for vuln in open_vulns))
    if limit:
        wheres = wheres[:limit]
    return wheres


async def get_where(loaders: Dataloaders, finding_id: str) -> str:
    """
    General locations of the Vulnerabilities. It is limited to 20 locations.
    """
    return ", ".join(sorted(await _get_wheres(loaders, finding_id, limit=20)))


async def has_access_to_finding(
    loaders: Dataloaders, email: str, finding_id: str
) -> bool | None:
    """Verify if the user has access to a finding submission."""
    finding: Finding | None = await loaders.finding.load(finding_id)
    if finding:
        return await authz.has_access_to_group(
            loaders, email, finding.group_name
        )
    raise FindingNotFound()


def is_deleted(finding: Finding) -> bool:
    return finding.state.status == FindingStateStatus.DELETED


async def mask_finding(
    loaders: Dataloaders, finding: Finding, email: str
) -> None:
    await comments_domain.remove_comments(finding_id=finding.id)
    await remove_all_evidences(finding.id, finding.group_name)

    vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding.id
    )
    await collect(
        tuple(
            vulns_domain.mask_vulnerability(
                loaders=loaders,
                email=email,
                finding_id=finding.id,
                vulnerability=vulnerability,
            )
            for vulnerability in vulnerabilities
        ),
        workers=8,
    )

    if finding.state.status == FindingStateStatus.DELETED and finding.approval:
        # Findings in the MASKED state will be archived by Streams
        # for analytics purposes
        await findings_model.update_state(
            current_value=finding.state,
            finding_id=finding.id,
            group_name=finding.group_name,
            state=finding.state._replace(
                modified_by=email,
                modified_date=datetime_utils.get_utc_now(),
                status=FindingStateStatus.MASKED,
            ),
        )

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


# Validate justification length and vet characters in it
@validations.validate_field_length_deco(
    "justification", limit=10, is_greater_than_limit=True
)
@validations.validate_field_length_deco(
    "justification", limit=10000, is_greater_than_limit=False
)
@validations.validate_fields_deco(["justification"])
async def request_vulnerabilities_verification(  # noqa pylint: disable=too-many-arguments, too-many-locals
    loaders: Dataloaders,
    finding_id: str,
    user_info: dict[str, str],
    justification: str,
    vulnerability_ids: set[str],
    is_closing_event: bool = False,
) -> None:
    finding = await get_finding(loaders, finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_vuln_ids(
        loaders,
        finding_id,
        vulnerability_ids,
    )
    vulnerabilities = list(
        await collect(
            tuple(
                vulns_utils.validate_requested_verification(
                    loaders, vuln, is_closing_event
                )
                for vuln in vulnerabilities
            )
        )
    )
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()
    root_ids = {
        vuln.root_id
        for vuln in vulnerabilities
        if vuln.root_id and not check_hold(vuln)
    }
    roots = await loaders.group_roots.load(finding.group_name)
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
    requester_email: str = user_info["user_email"]
    if is_closing_event:
        requester_email = (
            vulnerabilities[
                0
            ].unreliable_indicators.unreliable_last_reattack_requester
            or await vulns_domain.get_reattack_requester(
                loaders, vulnerabilities[0]
            )
            or requester_email
        )
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=requester_email,
        modified_date=datetime_utils.get_utc_now(),
        status=FindingVerificationStatus.REQUESTED,
        vulnerability_ids=vulnerability_ids,
    )
    await findings_model.update_verification(
        current_value=finding.verification,
        group_name=finding.group_name,
        finding_id=finding.id,
        verification=verification,
    )
    comment_data = FindingComment(
        finding_id=finding_id,
        comment_type=CommentType.VERIFICATION,
        content=justification,
        parent_id="0",
        id=comment_id,
        email=user_email,
        full_name=" ".join([user_info["first_name"], user_info["last_name"]]),
        creation_date=datetime_utils.get_utc_now(),
    )
    await comments_domain.add(loaders, comment_data)
    await collect(map(vulns_domain.request_verification, vulnerabilities))
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


async def repo_subtitle(
    loaders: Dataloaders, vuln: Vulnerability, group_name: str
) -> str:
    repo = "Vulnerabilities"
    if vuln.root_id is not None:
        try:
            root = await roots_domain.get_root(
                loaders, vuln.root_id, group_name
            )
            nickname = (
                root.state.nickname
                if isinstance(root.state.nickname, str)
                else repo
            )
            repo = (
                f"{nickname}/{root.state.branch}"
                if isinstance(root.state, (GitRootState, str))
                else nickname
            )
        except RootNotFound:
            repo = "Vulnerabilities"
    return repo


async def vulns_properties(
    loaders: Dataloaders,
    finding_id: str,
    vulnerabilities: list[Vulnerability],
    is_closed: bool = False,
) -> dict[str, Any]:
    finding = await get_finding(loaders, finding_id)
    vulns_props: dict[str, dict[str, dict[str, Any]]] = {}

    for vuln in vulnerabilities:
        repo = await repo_subtitle(loaders, vuln, finding.group_name)
        vuln_dict = vulns_props.get(repo, {})
        if is_closed:
            exposure: Decimal = 4 ** (get_severity_score(finding.severity) - 4)
            report_date = vuln.created_date.date()
            days_open = (
                datetime_utils.get_utc_now().date() - report_date
            ).days
            reattack_requester = (
                vuln.unreliable_indicators.unreliable_last_reattack_requester
            )
            vuln_dict.update(
                {
                    f"{vuln.state.where}{vuln.state.specific}": {
                        "location": vuln.state.where,
                        "specific": vuln.state.specific,
                        "source": vuln.state.source.value,
                        "assigned": vuln.treatment.assigned
                        if vuln.treatment
                        else None,
                        "report date": report_date,
                        "time to remediate": f"{days_open} calendar days",
                        "reattack requester": reattack_requester,
                        "reduction in exposure": round(exposure, 1),
                    },
                }
            )
        else:
            vuln_dict.update(
                {
                    f"{vuln.state.where}{vuln.state.specific}": {
                        "location": vuln.state.where,
                        "specific": vuln.state.specific,
                        "source": vuln.state.source.value,
                    },
                }
            )
        vulns_props[repo] = dict(sorted(vuln_dict.items()))

    return vulns_props


def get_remaining_exposure(
    finding: Finding, closed_vulnerabilities: int
) -> int:
    open_vulnerabilities = (
        finding.unreliable_indicators.unreliable_open_vulnerabilities
    )
    return int(
        (open_vulnerabilities - closed_vulnerabilities)
        * (4 ** (get_severity_score(finding.severity) - 4))
    )


@validations.validate_fields_deco(["description"])
@validations.validate_fields_length_deco(
    [
        "description.attack_vector_description",
        "description.description",
        "description.recommendation",
        "description.threat",
    ],
    limit=5000,
)
@validations.validate_fields_length_deco(
    [
        "description.attack_vector_description",
        "description.description",
        "description.recommendation",
        "description.threat",
    ],
    limit=0,
    is_greater_than_limit=True,
)
async def update_description(
    loaders: Dataloaders,
    finding_id: str,
    description: FindingDescriptionToUpdate,
) -> None:
    unfulfilled_requirements = (
        None
        if description.unfulfilled_requirements is None
        else sorted(set(description.unfulfilled_requirements))
    )
    if description.title:
        await findings_utils.is_valid_finding_title(loaders, description.title)

    finding = await get_finding(loaders, finding_id)
    if description.description is not None or description.threat is not None:
        await _validate_duplicated_finding(
            loaders,
            finding.group_name,
            description.title or finding.title,
            description.description or finding.description,
            description.threat or finding.threat,
            finding.severity,
            finding,
        )

    if unfulfilled_requirements is not None:
        await _validate_finding_requirements(
            loaders,
            description.title or finding.title,
            unfulfilled_requirements,
        )

    metadata = FindingMetadataToUpdate(
        attack_vector_description=description.attack_vector_description,
        description=description.description,
        recommendation=description.recommendation,
        sorts=description.sorts,
        threat=description.threat,
        title=description.title,
        unfulfilled_requirements=unfulfilled_requirements,
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def update_severity(
    loaders: Dataloaders,
    finding_id: str,
    severity: Finding20Severity | Finding31Severity,
) -> None:
    finding = await get_finding(loaders, finding_id)
    updated_severity: Finding20Severity | Finding31Severity
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

    await _validate_duplicated_finding(
        loaders,
        finding.group_name,
        finding.title,
        finding.description,
        finding.threat,
        updated_severity,
        finding,
    )
    metadata = FindingMetadataToUpdate(
        severity=updated_severity,
        severity_score=SeverityScore(
            base_score=cvss_utils.get_severity_base_score(updated_severity),
            temporal_score=cvss_utils.get_severity_temporal_score(
                updated_severity
            ),
            cvssf=cvss_utils.get_cvssf_score(
                cvss_utils.get_severity_temporal_score(updated_severity)
            ),
        ),
    )
    await findings_model.update_metadata(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def get_vuln_nickname(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> str:
    result: str = f"{vuln.state.where} ({vuln.state.specific})"
    try:
        root = await roots_domain.get_root(
            loaders, vuln.root_id or "", vuln.group_name
        )
        if vuln.type == "LINES":
            return f"  {root.state.nickname}/{result}"
    except RootNotFound:
        pass
    return result


async def add_reattack_justification(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    open_vulnerabilities: Iterable[Vulnerability],
    closed_vulnerabilities: Iterable[Vulnerability],
    commit_hash: str | None = None,
    comment_type: CommentType = CommentType.COMMENT,
    email: str = "machine@fluidttacks.com",
    full_name: str = "Machine Services",
    observations: str | None = None,
) -> None:
    justification = (
        datetime.now(tz=timezone.utc)
        .astimezone(tz=pytz.timezone(TIME_ZONE))
        .strftime("%Y/%m/%d %H:%M")
    )
    commit_msg = f" in commit {commit_hash}" if commit_hash else ""
    observations_msg = (
        f"\n\nObservations:\n {observations}" if observations else ""
    )
    justification = (
        "A reattack request was executed on "
        f"{justification.replace(' ', ' at ')}{commit_msg}."
    )
    vulns_strs = [
        f"  - {await get_vuln_nickname(loaders, vuln)}"
        for vuln in open_vulnerabilities
    ]
    if vulns_strs:
        justification += "\n\nOpen vulnerabilities:\n"
        justification += "\n".join(vulns_strs) if vulns_strs else ""
    vulns_strs = [
        f"  - {await get_vuln_nickname(loaders, vuln)}"
        for vuln in closed_vulnerabilities
    ]
    if vulns_strs:
        justification += "\n\nClosed vulnerabilities:\n"
        justification += "\n".join(vulns_strs) if vulns_strs else ""
    justification += observations_msg
    LOGGER.info(
        "%s Vulnerabilities were verified and found open in finding %s",
        len(list(open_vulnerabilities)),
        finding_id,
    )
    LOGGER.info(
        "%s Vulnerabilities were verified and found closed in finding %s",
        len(list(closed_vulnerabilities)),
        finding_id,
    )
    if open_vulnerabilities or closed_vulnerabilities:
        closed_properties: VulnsProperties | None = None
        if closed_vulnerabilities:
            finding = await get_finding(loaders, finding_id)
            if finding.state.status == FindingStateStatus.APPROVED:
                closed_properties = VulnsProperties(
                    remaining_exposure=get_remaining_exposure(
                        finding, len(list(closed_vulnerabilities))
                    ),
                    severity_level=get_severity_level(
                        get_severity_score(finding.severity)
                    ),
                    severity_score=get_severity_score(finding.severity),
                    vulns_props=await vulns_properties(
                        loaders,
                        finding_id,
                        [
                            vuln
                            for vuln in closed_vulnerabilities
                            if vuln is not None
                        ],
                        is_closed=True,
                    ),
                )
        await comments_domain.add(
            loaders,
            FindingComment(
                finding_id=finding_id,
                id=str(round(time() * 1000)),
                comment_type=comment_type,
                parent_id="0",
                creation_date=datetime_utils.get_utc_now(),
                full_name=full_name,
                content=justification,
                email=email,
            ),
            closed_properties=closed_properties,
        )


# Validate justification length and vet characters in it
@validations.validate_field_length_deco(
    "justification",
    limit=10,
    is_greater_than_limit=True,
)
@validations.validate_field_length_deco(
    "justification",
    limit=10000,
    is_greater_than_limit=False,
)
@validations.validate_fields_deco(["justification"])
async def verify_vulnerabilities(  # pylint: disable=too-many-locals
    *,
    context: Any | None = None,
    finding_id: str,
    user_info: dict[str, str],
    justification: str,
    open_vulns_ids: list[str],
    closed_vulns_ids: list[str],
    vulns_to_close_from_file: list[Vulnerability],
    loaders: Dataloaders,
    is_reattack_open: bool | None = None,
    is_closing_event: bool = False,
) -> None:
    # All vulns must be open before verifying them
    # we will just keep them open or close them
    # in either case, their historic_verification is updated to VERIFIED
    loaders.finding.clear(finding_id)
    finding = await get_finding(loaders, finding_id)
    if context and not operation_can_be_executed(context, finding.title):
        raise MachineCanNotOperate()

    vulnerability_ids = open_vulns_ids + closed_vulns_ids
    vulnerabilities = [
        vuln
        for vuln in await loaders.finding_vulnerabilities_all.load(finding_id)
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
    today = datetime_utils.get_utc_now()
    modified_by = user_info["user_email"]

    # Modify the verification state to mark the finding as verified
    verification = FindingVerification(
        comment_id=comment_id,
        modified_by=modified_by,
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

    if is_reattack_open is None:
        open_vulnerabilities = await vulns_domain.get_vulnerabilities(
            loaders, open_vulns_ids
        )
        closed_vulnerabilities = await vulns_domain.get_vulnerabilities(
            loaders, closed_vulns_ids
        )
        await add_reattack_justification(
            loaders=loaders,
            finding_id=finding_id,
            open_vulnerabilities=open_vulnerabilities,
            closed_vulnerabilities=closed_vulnerabilities,
            comment_type=CommentType.VERIFICATION,
            email=modified_by,
            full_name=" ".join(
                [user_info["first_name"], user_info["last_name"]]
            ),
            observations=justification,
        )
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


async def get_oldest_no_treatment(
    loaders: Dataloaders,
    findings: Iterable[Finding],
) -> dict[str, int | str] | None:
    """Get the finding with oldest "no treatment" vulnerability."""
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            [finding.id for finding in findings]
        )
    )
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    no_treatment_vulns = vulns_utils.filter_no_treatment_vulns(open_vulns)
    if not no_treatment_vulns:
        return None
    treatment_dates: list[datetime] = [
        vuln.treatment.modified_date
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
    loaders: Dataloaders,
    finding_id: str,
) -> datetime | None:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)

    return min(report_dates) if report_dates else None


async def get_oldest_vulnerability_report_date(
    loaders: Dataloaders,
    finding_id: str,
) -> datetime | None:
    vulns = await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    report_dates = vulns_utils.get_report_dates(
        vulns_utils.filter_released_vulns(vulns)
    )

    return min(report_dates) if report_dates else None


async def get_vulnerabilities_to_reattack(
    loaders: Dataloaders,
    finding_id: str,
) -> list[Vulnerability]:
    finding_vulns = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    return vulns_utils.filter_open_vulns(
        vulns_utils.filter_remediated(finding_vulns)
    )


def check_hold(vuln: Vulnerability) -> bool:
    return (
        vuln.verification is not None
        and vuln.verification.status == VulnerabilityVerificationStatus.ON_HOLD
    )
