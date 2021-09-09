# pylint: disable=too-many-lines

import aioboto3
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    in_process,
    schedule,
)
import authz
from botocore.exceptions import (
    ClientError,
)
import bugsnag
from comments import (
    domain as comments_domain,
)
from context import (
    FI_API_STATUS,
)
from contextlib import (
    AsyncExitStack,
)
from custom_exceptions import (
    FindingNotFound,
    InvalidCommentParent,
    InvalidDraftTitle,
    NotVerificationRequested,
    PermissionDenied,
    UnavailabilityError,
    VulnNotFound,
)
from custom_types import (
    Comment as CommentType,
    Finding as FindingType,
    Tracking as TrackingItem,
    Vulnerability as VulnerabilityType,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
)
from db_model.findings.enums import (
    FindingStateJustification,
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingMetadataToUpdate,
    FindingState,
    FindingVerification,
)
from decimal import (
    Decimal,
)
from dynamodb.operations_legacy import (
    start_context,
)
from findings import (
    dal as findings_dal,
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
from newutils import (
    cvss,
    cvss_new,
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
    token as token_utils,
    utils,
    validations,
    vulnerabilities as vulns_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from newutils.vulnerabilities import (
    Treatments,
)
from operator import (
    itemgetter,
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
    cast,
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


def cast_new_vulnerabilities(
    finding_new: Dict[str, FindingType], finding: Dict[str, FindingType]
) -> Dict[str, FindingType]:
    """Cast values for new format."""
    if int(str(finding_new.get("openVulnerabilities"))) >= 0:
        finding["openVulnerabilities"] = str(
            finding_new.get("openVulnerabilities")
        )
    else:
        # This finding does not have open vulnerabilities
        pass
    where = "-"
    if finding_new.get("portsVulns"):
        finding["portsVulns"] = vulns_utils.group_specific(
            cast(List[Dict[str, str]], finding_new.get("portsVulns")), "ports"
        )
        where = vulns_utils.format_where(
            where, cast(List[Dict[str, str]], finding["portsVulns"])
        )
    else:
        # This finding does not have ports vulnerabilities
        pass
    if finding_new.get("linesVulns"):
        finding["linesVulns"] = vulns_utils.group_specific(
            cast(List[Dict[str, str]], finding_new.get("linesVulns")), "lines"
        )
        where = vulns_utils.format_where(
            where, cast(List[Dict[str, str]], finding["linesVulns"])
        )
    else:
        # This finding does not have lines vulnerabilities
        pass
    if finding_new.get("inputsVulns"):
        finding["inputsVulns"] = vulns_utils.group_specific(
            cast(List[str], finding_new.get("inputsVulns")), "inputs"
        )
        where = vulns_utils.format_where(
            where, cast(List[Dict[str, str]], finding["inputsVulns"])
        )
    else:
        # This finding does not have inputs vulnerabilities
        pass
    finding["where"] = where
    return finding


async def remove_finding(
    context: Any, finding_id: str, justification: str
) -> bool:
    finding = await get_finding(finding_id)
    submission_history = cast(
        List[Dict[str, str]], finding.get("historicState", [{}])
    )
    success = False

    if submission_history[-1].get("state") != "DELETED":
        delete_date = datetime_utils.get_now_as_str()
        user_info = await token_utils.get_jwt_content(context)
        analyst = user_info["user_email"]
        source = requests_utils.get_source(context)
        submission_history.append(
            {
                "state": "DELETED",
                "date": delete_date,
                "justification": justification,
                "analyst": analyst,
                "source": source,
            }
        )
        success = await findings_dal.update(
            finding_id, {"historic_state": submission_history}
        )
        schedule(
            remove_vulnerabilities(context, finding_id, justification, analyst)
        )
        group_name = get_key_or_fallback(finding, "groupName", "projectName")
        file_names = await findings_dal.search_evidence(
            f"{group_name}/{finding_id}"
        )
        await collect(
            findings_dal.remove_evidence(file_name) for file_name in file_names
        )
        await findings_dal.update(finding_id, {"files": []})
    return success


async def remove_finding_new(
    context: Any,
    finding_id: str,
    justification: FindingStateJustification,
    user_email: str,
) -> None:
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    new_state = FindingState(
        justification=justification,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.DELETED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
    schedule(
        remove_vulnerabilities(
            context, finding_id, justification.value, user_email
        )
    )
    file_names = await findings_dal.search_evidence(
        f"{finding.group_name}/{finding.id}"
    )
    await collect(
        findings_dal.remove_evidence(file_name) for file_name in file_names
    )
    metadata = FindingMetadataToUpdate(evidences=FindingEvidences())
    await findings_model.update_medatada(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def remove_vulnerabilities(
    context: Any, finding_id: str, justification: str, user_email: str
) -> bool:
    finding_vulns_loader = context.loaders.finding_vulns
    vulnerabilities = await finding_vulns_loader.load(finding_id)
    source = requests_utils.get_source(context)
    return all(
        await collect(
            vulns_domain.remove_vulnerability(
                context.loaders,
                finding_id,
                str(vuln["UUID"]),
                justification,
                user_email,
                source,
                include_closed_vuln=True,
            )
            for vuln in vulnerabilities
        )
    )


def filter_zero_risk_vulns(
    vulns: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    vulns_filter_non_confirm_zero = vulns_utils.filter_non_confirmed_zero_risk(
        vulns
    )
    return vulns_utils.filter_non_requested_zero_risk(
        vulns_filter_non_confirm_zero
    )


async def get(
    finding_id: str, table: aioboto3.session.Session.client
) -> Dict[str, FindingType]:
    finding = await findings_dal.get(finding_id, table)
    if not finding or not await validate_finding(finding=finding):
        raise FindingNotFound()
    return findings_utils.format_data(finding)


async def get_attributes(
    finding_id: str, attributes: List[str]
) -> Dict[str, FindingType]:
    if "finding_id" not in attributes:
        attributes = [*attributes, "finding_id"]
    response = await findings_dal.get_attributes(finding_id, attributes)
    if not response:
        raise FindingNotFound()
    return response


async def get_closed_vulnerabilities(loaders: Any, finding_id: str) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulns: List[VulnerabilityType] = await finding_vulns_loader.load(
        finding_id
    )
    vulns = vulns_domain.filter_closed_vulnerabilities(vulns)
    return len(vulns)


async def get_finding(finding_id: str) -> Dict[str, FindingType]:
    """Retrieves and formats finding attributes"""
    finding = await findings_dal.get_finding(finding_id)
    if not finding or not await validate_finding(finding=finding):
        raise FindingNotFound()
    return findings_utils.format_data(finding)


async def get_finding_age(context: Any, finding_id: str) -> int:
    age = 0
    finding_vulns_loader: DataLoader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    report_dates = vulns_utils.get_report_dates(vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        age = (datetime_utils.get_now() - oldest_report_date).days
    return age


async def get_finding_last_vuln_report(context: Any, finding_id: str) -> int:
    last_vuln_report = 0
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    report_dates = vulns_utils.get_report_dates(vulns)
    if report_dates:
        newest_report_date = max(report_dates)
        last_vuln_report = (datetime_utils.get_now() - newest_report_date).days
    return last_vuln_report


async def get_finding_open_age(context: Any, finding_id: str) -> int:
    open_age = 0
    finding_vulns_loader = context.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    report_dates = vulns_utils.get_report_dates(open_vulns)
    if report_dates:
        oldest_report_date = min(report_dates)
        open_age = (datetime_utils.get_now() - oldest_report_date).days
    return open_age


async def get_findings_async(
    finding_ids: List[str],
) -> List[Dict[str, FindingType]]:
    """Retrieves all attributes for the requested findings"""
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(findings_dal.TABLE_NAME)
        findings = await collect(
            [get(finding_id, table) for finding_id in finding_ids]
        )
    return cast(List[Dict[str, FindingType]], findings)


async def get_findings_by_group(
    group_name: str,
    attrs: Optional[Set[str]] = None,
    include_deleted: bool = False,
) -> List[Dict[str, FindingType]]:
    if attrs and "historic_state" not in attrs:
        attrs.add("historic_state")
    findings = await findings_dal.get_findings_by_group(group_name, attrs)
    findings = findings_utils.filter_non_created_findings(findings)
    findings = findings_utils.filter_non_rejected_findings(findings)
    findings = findings_utils.filter_non_submitted_findings(findings)

    if not include_deleted:
        findings = findings_utils.filter_non_deleted_findings(findings)
    return [
        findings_utils.format_finding(finding, attrs) for finding in findings
    ]


async def get_last_closed_vulnerability_info(
    context: Any, findings: List[Dict[str, FindingType]]
) -> Tuple[Decimal, VulnerabilityType]:
    """Get days since the last closed vulnerability"""
    validate_findings = await collect(
        [validate_finding(finding=finding) for finding in findings]
    )
    validated_findings = [
        finding
        for finding, is_valid in zip(findings, validate_findings)
        if is_valid
    ]
    vulns = await context.finding_vulns_nzr.load_many_chained(
        [str(finding["finding_id"]) for finding in validated_findings]
    )
    are_vuln_closed = [
        vulns_utils.is_vulnerability_closed(vuln) for vuln in vulns
    ]
    closed_vulnerabilities = [
        vuln
        for vuln, is_vuln_closed in zip(vulns, are_vuln_closed)
        if is_vuln_closed
    ]
    closing_vuln_dates = [
        vulns_utils.get_last_closing_date(vuln)
        for vuln in closed_vulnerabilities
    ]
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i) for i, v in enumerate(closing_vuln_dates)
        )
        last_closed_vuln = closed_vulnerabilities[date_index]
        current_date = max(closing_vuln_dates)
        last_closed_days = Decimal(
            (datetime_utils.get_now().date() - current_date).days
        ).quantize(Decimal("0.1"))
    else:
        last_closed_days = Decimal(0)
        last_closed_vuln = {}
    return last_closed_days, cast(VulnerabilityType, last_closed_vuln)


async def get_last_closed_vulnerability_info_new(
    loaders: Any,
    findings: Tuple[Finding, ...],
) -> Tuple[Decimal, VulnerabilityType]:
    """Get days since the last closed vulnerability"""
    finding_vulns_loader = loaders.finding_vulns_nzr
    valid_findings_ids = [
        finding.id for finding in findings if not is_deleted_new(finding)
    ]
    vulns = await finding_vulns_loader.load_many_chained(valid_findings_ids)
    are_vuln_closed = [
        vulns_utils.is_vulnerability_closed(vuln) for vuln in vulns
    ]
    closed_vulnerabilities = [
        vuln
        for vuln, is_vuln_closed in zip(vulns, are_vuln_closed)
        if is_vuln_closed
    ]
    closing_vuln_dates = [
        vulns_utils.get_last_closing_date(vuln)
        for vuln in closed_vulnerabilities
    ]
    if closing_vuln_dates:
        current_date, date_index = max(
            (v, i) for i, v in enumerate(closing_vuln_dates)
        )
        last_closed_vuln = closed_vulnerabilities[date_index]
        current_date = max(closing_vuln_dates)
        last_closed_days = Decimal(
            (datetime_utils.get_now().date() - current_date).days
        ).quantize(Decimal("0.1"))
    else:
        last_closed_days = Decimal(0)
        last_closed_vuln = {}
    return last_closed_days, cast(VulnerabilityType, last_closed_vuln)


async def get_group(finding_id: str) -> str:
    attribute = await get_attributes(finding_id, ["project_name"])
    return str(get_key_or_fallback(attribute))


async def get_is_verified(loaders: Any, finding_id: str) -> bool:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulns: List[VulnerabilityType] = await finding_vulns_loader.load(
        finding_id
    )
    vulns = vulns_domain.filter_open_vulnerabilities(vulns)
    remediated_vulns = vulns_domain.filter_remediated(vulns)
    return len(remediated_vulns) == 0


async def get_max_open_severity(
    context: Any, findings: List[Dict[str, FindingType]]
) -> Tuple[Decimal, Dict[str, FindingType]]:
    total_vulns = await collect(
        [total_vulnerabilities(context, fin) for fin in findings], workers=12
    )
    opened_findings = [
        finding
        for finding, total_vuln in zip(findings, total_vulns)
        if int(total_vuln.get("openVulnerabilities", "")) > 0
    ]
    total_severity: List[float] = cast(
        List[float],
        [finding.get("cvss_temporal", 0.0) for finding in opened_findings],
    )
    if total_severity:
        severity, severity_index = max(
            (v, i) for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal("0.1"))
        max_severity_finding = opened_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal("0.1"))
        max_severity_finding = {}
    return max_severity, max_severity_finding


async def get_max_open_severity_new(
    loaders: Any, findings: Tuple[Finding, ...]
) -> Tuple[Decimal, Optional[Finding]]:
    total_vulns = await collect(
        [total_vulnerabilities_new(loaders, finding) for finding in findings]
    )
    opened_findings = [
        finding
        for finding, total_vuln in zip(findings, total_vulns)
        if int(total_vuln.get("openVulnerabilities", "")) > 0
    ]
    total_severity: List[float] = cast(
        List[float],
        [
            float(get_severity_score_new(finding.severity))
            for finding in opened_findings
        ],
    )
    if total_severity:
        severity, severity_index = max(
            (v, i) for i, v in enumerate(total_severity)
        )
        max_severity = Decimal(severity).quantize(Decimal("0.1"))
        max_severity_finding = opened_findings[severity_index]
    else:
        max_severity = Decimal(0).quantize(Decimal("0.1"))
        max_severity_finding = None
    return max_severity, max_severity_finding


async def get_open_vulnerabilities(loaders: Any, finding_id: str) -> int:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulns: List[VulnerabilityType] = await finding_vulns_loader.load(
        finding_id
    )
    vulns = vulns_domain.filter_open_vulnerabilities(vulns)
    return len(vulns)


async def get_pending_verification_findings(
    context: Any, group_name: str
) -> List[Dict[str, FindingType]]:
    """Gets findings pending for verification"""
    findings_ids = await list_findings(context, [group_name])
    are_pending_verifications = await collect(
        [
            is_pending_verification(context, finding_id)
            for finding_id in findings_ids[0]
        ]
    )
    pending_to_verify_ids = [
        finding_id
        for finding_id, are_pending_verification in zip(
            findings_ids[0], are_pending_verifications
        )
        if are_pending_verification
    ]
    pending_to_verify = await collect(
        get_attributes(finding_id, ["finding", "finding_id", "project_name"])
        for finding_id in pending_to_verify_ids
    )
    return cast(List[Dict[str, FindingType]], pending_to_verify)


async def get_pending_verification_findings_new(
    loaders: Any,
    group_name: str,
) -> List[Dict[str, str]]:
    """Gets findings pending for verification"""
    findings_ids = await list_findings_new(loaders, [group_name])
    are_pending_verifications = await collect(
        [
            is_pending_verification_new(loaders, finding_id)
            for finding_id in findings_ids[0]
        ]
    )
    pending_to_verify_ids = [
        finding_id
        for finding_id, are_pending_verification in zip(
            findings_ids[0], are_pending_verifications
        )
        if are_pending_verification
    ]
    findings_loader = loaders.finding_new
    findings_to_verify: Tuple[
        Finding, ...
    ] = await findings_loader.load_many_chained(pending_to_verify_ids)
    pending_to_verify = await collect(
        {
            "title": finding.title,
            "id": finding.id,
            "group_name": finding.group_name,
        }
        for finding in findings_to_verify
    )
    return cast(List[Dict[str, str]], pending_to_verify)


async def get_report_date_new(loaders: Any, finding_id: str) -> Optional[str]:
    iso_report_date = ""
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    report_dates = vulns_utils.get_report_dates(vulns)
    if report_dates:
        report_date = min(report_dates)
        iso_report_date = datetime_utils.get_as_utc_iso_format(report_date)

    return iso_report_date


def get_severity_score_new(
    severity: Union[Finding20Severity, Finding31Severity]
) -> Decimal:
    if isinstance(severity, Finding31Severity):
        base_score = cvss_new.get_cvss3_basescore(severity)
        return cvss_new.get_cvss3_temporal(severity, base_score)

    base_score = cvss_new.get_cvss2_basescore(severity)
    return cvss_new.get_cvss2_temporal(severity, base_score)


async def get_status(loaders: Any, finding_id: str) -> str:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    open_vulns = vulns_domain.filter_open_vulnerabilities(vulns)
    return "open" if open_vulns else "closed"


async def get_total_treatment(
    context: Any, findings: List[Dict[str, FindingType]]
) -> Dict[str, int]:
    """Get the total treatment of all the vulnerabilities"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    finding_vulns_loader = context.finding_vulns_nzr

    are_findings_valid = await collect(
        [validate_finding(finding=finding) for finding in findings]
    )
    valid_findings = [
        finding
        for finding, is_finding_valid in zip(findings, are_findings_valid)
        if is_finding_valid
    ]
    vulns = await finding_vulns_loader.load_many_chained(
        [str(finding["finding_id"]) for finding in valid_findings]
    )

    for vuln in vulns:
        vuln_treatment = cast(
            List[Dict[str, str]], vuln.get("historic_treatment", [{}])
        )[-1].get("treatment")
        current_state = vulns_utils.get_last_status(vuln)
        open_vuln: int = 1 if current_state == "open" else 0
        if vuln_treatment == "ACCEPTED":
            accepted_vuln += open_vuln
        elif vuln_treatment == "ACCEPTED_UNDEFINED":
            indefinitely_accepted_vuln += open_vuln
        elif vuln_treatment == "IN PROGRESS":
            in_progress_vuln += open_vuln
        else:
            undefined_treatment += open_vuln
    return {
        "accepted": accepted_vuln,
        "acceptedUndefined": indefinitely_accepted_vuln,
        "inProgress": in_progress_vuln,
        "undefined": undefined_treatment,
    }


async def get_total_treatment_new(
    loaders: Any, findings: Tuple[Finding, ...]
) -> Dict[str, int]:
    """Get the total vulnerability treatment of all the findings"""
    accepted_vuln: int = 0
    indefinitely_accepted_vuln: int = 0
    in_progress_vuln: int = 0
    undefined_treatment: int = 0
    finding_vulns_loader = loaders.finding_vulns_nzr

    valid_findings = [
        finding for finding in findings if not is_deleted_new(finding)
    ]
    vulns = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in valid_findings]
    )

    for vuln in vulns:
        vuln_treatment = cast(
            List[Dict[str, str]], vuln.get("historic_treatment", [{}])
        )[-1].get("treatment")
        current_state = vulns_utils.get_last_status(vuln)
        open_vuln: int = 1 if current_state == "open" else 0
        if vuln_treatment == "ACCEPTED":
            accepted_vuln += open_vuln
        elif vuln_treatment == "ACCEPTED_UNDEFINED":
            indefinitely_accepted_vuln += open_vuln
        elif vuln_treatment == "IN PROGRESS":
            in_progress_vuln += open_vuln
        else:
            undefined_treatment += open_vuln
    return {
        "accepted": accepted_vuln,
        "acceptedUndefined": indefinitely_accepted_vuln,
        "inProgress": in_progress_vuln,
        "undefined": undefined_treatment,
    }


def get_tracking_vulnerabilities(
    vulnerabilities: List[Dict[str, FindingType]]
) -> List[TrackingItem]:
    """get tracking vulnerabilities dictionary"""
    filter_deleted_status = [
        vulns_utils.filter_deleted_status(vuln) for vuln in vulnerabilities
    ]
    vulns_filtered = [
        findings_utils.clean_deleted_state(vuln)
        for vuln, filter_deleted in zip(vulnerabilities, filter_deleted_status)
        if filter_deleted
    ]
    vulns_filtered_zero = filter_zero_risk_vulns(vulns_filtered)
    states_actions = findings_utils.get_state_actions(vulns_filtered_zero)
    treatments_actions = findings_utils.get_treatment_actions(
        vulns_filtered_zero
    )

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
            open=action.times if action.action == "open" else 0,
            closed=action.times if action.action == "closed" else 0,
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


async def get_treatment_summary(loaders: Any, finding_id: str) -> Treatments:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulnerabilities: List[VulnerabilityType] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulnerabilities = vulns_domain.filter_open_vulnerabilities(
        vulnerabilities
    )
    return vulns_utils.get_treatments(open_vulnerabilities)


def get_updated_evidence_date_new(
    finding: Finding, evidence: FindingEvidence
) -> datetime:
    evidence_date = datetime.fromisoformat(evidence.modified_date)
    updated_date = evidence_date
    if finding.approval:
        release_date = datetime.fromisoformat(finding.approval.modified_date)
        if release_date > evidence_date:
            updated_date = release_date
    return updated_date


async def get_where(loaders: Any, finding_id: str) -> str:
    """
    General locations of the Vulnerabilities. It is limited to 20 locations.
    """
    return ", ".join(await get_wheres(loaders, finding_id, limit=20))


async def get_wheres(
    loaders: Any, finding_id: str, limit: Optional[int] = None
) -> List[str]:
    finding_vulns_loader: DataLoader = loaders.finding_vulns_nzr
    vulnerabilities: List[VulnerabilityType] = await finding_vulns_loader.load(
        finding_id
    )
    open_vulnerabilities = vulns_domain.filter_open_vulnerabilities(
        vulnerabilities
    )
    wheres = sorted(
        set(
            map(
                lambda vulnerability: vulnerability["where"],
                open_vulnerabilities,
            )
        )
    )
    if limit:
        wheres = wheres[:limit]

    return wheres


async def has_access_to_finding(email: str, finding_id: str) -> bool:
    """Verify if the user has access to a finding submission."""
    finding = await get_finding(finding_id)
    group = cast(str, finding.get("projectName", ""))
    return await authz.has_access_to_group(email, group)


def is_deleted(finding: Dict[str, FindingType]) -> bool:
    historic_state = cast(
        List[Dict[str, str]], finding.get("historic_state", [{}])
    )
    return historic_state[-1].get("state", "") == "DELETED"


def is_deleted_new(finding: Finding) -> bool:
    return finding.state.status == FindingStateStatus.DELETED


async def is_pending_verification(context: Any, finding_id: str) -> bool:
    finding_loader = context.finding_vulns_nzr
    vulns = await finding_loader.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    reattack_requested = [
        vuln
        for vuln in open_vulns
        if cast(List[Dict[str, str]], vuln.get("historic_verification", [{}]))[
            -1
        ].get("status")
        == "REQUESTED"
    ]
    return len(reattack_requested) > 0 and await validate_finding(finding_id)


async def is_pending_verification_new(
    loaders: Any,
    finding_id: str,
) -> bool:
    # Validate if finding exists
    finding_loader = loaders.finding_new
    await finding_loader.load(finding_id)

    finding_vulns_loader = loaders.finding_vulns_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    open_vulns = vulns_utils.filter_open_vulns(vulns)
    reattack_requested = [
        vuln
        for vuln in open_vulns
        if cast(List[Dict[str, str]], vuln.get("historic_verification", [{}]))[
            -1
        ].get("status")
        == "REQUESTED"
    ]
    return len(reattack_requested) > 0


async def list_findings(
    context: Any, group_names: List[str], include_deleted: bool = False
) -> List[List[str]]:
    """Returns a list of the list of finding ids associated with the groups"""
    group_findings_loader = (
        context.group_findings_all
        if include_deleted
        else context.group_findings
    )
    findings = await group_findings_loader.load_many(group_names)
    findings = [
        list(map(lambda finding: finding["finding_id"], group_findings))
        for group_findings in findings
    ]
    return cast(List[List[str]], findings)


async def list_findings_new(
    loaders: Any,
    group_names: List[str],
    include_deleted: bool = False,
) -> List[List[str]]:
    """Returns a list of the list of finding ids associated with the groups"""
    group_findings_loader = (
        loaders.group_findings_all_new
        if include_deleted
        else loaders.group_findings_new
    )
    findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await group_findings_loader.load_many(group_names)
    findings_ids = [
        list(map(lambda finding: finding.id, group_findings))
        for group_findings in findings
    ]
    return cast(List[List[str]], findings_ids)


async def mask_finding(  # pylint: disable=too-many-locals
    context: Any, finding_id: str
) -> bool:
    finding = await findings_dal.get_finding(finding_id)
    finding = findings_utils.format_data(finding)
    historic_verification = cast(
        List[Dict[str, str]], finding.get("historicVerification", [])
    )

    attrs_to_mask = [
        "affected_systems",
        "attack_vector_desc",
        "effect_solution",
        "related_findings",
        "risk",
        "threat",
        "treatment",
        "treatment_manager",
        "vulnerability",
        "records",
    ]
    mask_finding_coroutines = [
        findings_dal.update(
            finding_id, {attr: "Masked" for attr in attrs_to_mask}
        )
    ]

    mask_finding_coroutines.append(
        mask_verification(finding_id, historic_verification)
    )

    list_evidences_files = await findings_dal.search_evidence(
        f'{finding["projectName"]}/{finding_id}'
    )
    evidence_s3_coroutines = [
        findings_dal.remove_evidence(file_name)
        for file_name in list_evidences_files
    ]

    evidence_dynamodb_coroutine = findings_dal.update(
        finding_id,
        {
            "files": [
                {
                    "file_url": "Masked",
                    "name": "Masked",
                    "description": "Masked",
                }
                for _ in cast(List[Dict[str, str]], finding["evidence"])
            ]
        },
    )
    mask_finding_coroutines.append(evidence_dynamodb_coroutine)

    comments_and_observations = await comments_domain.get(
        "comment", finding_id
    ) + await comments_domain.get("observation", finding_id)
    comments_coroutines = [
        comments_domain.delete(comment["comment_id"], finding_id)
        for comment in comments_and_observations
    ]
    mask_finding_coroutines.extend(comments_coroutines)

    finding_all_vulns_loader = context.finding_vulns_all
    vulns = await finding_all_vulns_loader.load(finding_id)
    mask_vulns_coroutines = [
        vulns_domain.mask_vuln(finding_id, str(vuln["UUID"])) for vuln in vulns
    ]
    mask_finding_coroutines.extend(mask_vulns_coroutines)

    try:
        success = all(await collect(mask_finding_coroutines))
        await collect(evidence_s3_coroutines)
    except ClientError as ex:
        raise UnavailabilityError() from ex
    finally:
        if not success:
            bugsnag.notify(
                Exception("Failed to mask finding"), severity="Error"
            )
    return success


async def mask_finding_new(  # pylint: disable=too-many-locals
    loaders: Any, finding: Finding
) -> bool:
    mask_finding_coroutines = []
    mask_new_finding_coroutines = []
    masked_msg = "Masked"
    new_evidences = finding.evidences._replace(
        **{
            evidence_name: evidence._replace(
                description=masked_msg, url=masked_msg
            )
            for evidence_name in finding.evidences._fields
            for evidence in [getattr(finding.evidences, evidence_name)]
            if evidence
        }
    )
    metadata = FindingMetadataToUpdate(
        affected_systems=masked_msg,
        attack_vector_description=masked_msg,
        compromised_attributes=masked_msg,
        description=masked_msg,
        evidences=new_evidences,
        recommendation=masked_msg,
        risk=masked_msg,
        threat=masked_msg,
    )
    mask_new_finding_coroutines.append(
        findings_model.update_medatada(
            group_name=finding.group_name,
            finding_id=finding.id,
            metadata=metadata,
        )
    )
    finding_historic_verification_loader = (
        loaders.finding_historic_verification_new
    )
    finding_historic_verification: Tuple[
        FindingVerification, ...
    ] = await finding_historic_verification_loader.load(finding.id)
    new_historic_verification = tuple(
        verification._replace(
            status=FindingVerificationStatus.MASKED, modified_by=masked_msg
        )
        for verification in finding_historic_verification
    )
    mask_new_finding_coroutines.append(
        findings_model.update_historic_verification(
            group_name=finding.group_name,
            finding_id=finding.id,
            historic_verification=new_historic_verification,
        )
    )
    list_evidences_files = await findings_dal.search_evidence(
        f"{finding.group_name}/{finding.id}"
    )
    evidence_s3_coroutines = [
        findings_dal.remove_evidence(file_name)
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
    finding_all_vulns_loader = loaders.finding_vulns_all
    vulns = await finding_all_vulns_loader.load(finding.id)
    mask_vulns_coroutines = [
        vulns_domain.mask_vuln(finding.id, str(vuln["UUID"])) for vuln in vulns
    ]
    mask_finding_coroutines.extend(mask_vulns_coroutines)
    await collect(mask_new_finding_coroutines)
    return all(await collect(mask_finding_coroutines))


async def mask_verification(
    finding_id: str, historic_verification: List[Dict[str, str]]
) -> bool:
    historic = [
        {**treatment, "status": "Masked", "user": "Masked"}
        for treatment in historic_verification
    ]
    return await findings_dal.update(
        finding_id, {"historic_verification": historic}
    )


async def request_vulnerabilities_verification(
    context: Any,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vuln_ids: List[str],
) -> None:
    finding = await findings_dal.get_finding(finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_uuids(
        finding_id, set(vuln_ids)
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
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info["user_email"]
    historic_verification = cast(
        List[Dict[str, Union[str, int, List[str]]]],
        finding.get("historic_verification", []),
    )
    historic_verification.append(
        {
            "comment": comment_id,
            "date": today,
            "status": "REQUESTED",
            "user": user_email,
            "vulns": vuln_ids,
        }
    )
    update_finding = await findings_dal.update(
        finding_id, {"historic_verification": historic_verification}
    )
    comment_data = {
        "comment_type": "verification",
        "content": justification,
        "parent": "0",
        "comment_id": comment_id,
    }
    await comments_domain.add(finding_id, comment_data, user_info)

    update_vulns = await collect(
        map(vulns_domain.request_verification, vulnerabilities)
    )
    if all(update_vulns) and update_finding:
        schedule(
            findings_mail.send_mail_remediate_finding(
                context,
                user_email,
                finding_id,
                str(finding.get("finding", "")),
                str(finding.get("project_name", "")),
                justification,
            )
        )

    else:
        LOGGER.error("An error occurred remediating", **NOEXTRA)
        raise NotVerificationRequested()


async def request_vulnerabilities_verification_new(
    context: Any,
    finding_id: str,
    user_info: Dict[str, str],
    justification: str,
    vulnerability_ids: Set[str],
) -> None:
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    vulnerabilities = await vulns_domain.get_by_finding_and_uuids(
        finding_id, vulnerability_ids
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
    update_vulns = await collect(
        map(vulns_domain.request_verification, vulnerabilities)
    )
    if not all(update_vulns):
        LOGGER.error("An error occurred remediating", **NOEXTRA)
        raise NotVerificationRequested()

    schedule(
        findings_mail.send_mail_remediate_finding(
            context.loaders,
            user_email,
            finding.id,
            finding.title,
            finding.group_name,
            justification,
        )
    )


async def save_severity(finding: Dict[str, FindingType]) -> bool:
    """Organize severity metrics to save in dynamo."""
    cvss_version: str = str(finding.get("cvssVersion", ""))
    cvss_parameters = findings_utils.CVSS_PARAMETERS[cvss_version]
    severity = cvss.calculate_severity(cvss_version, finding, cvss_parameters)
    response = await findings_dal.update(str(finding.get("id", "")), severity)
    return response


async def total_vulnerabilities(
    context: Any, finding_: Dict[str, FindingType]
) -> Dict[str, int]:
    finding_id: str = str(finding_["finding_id"])
    finding = {"openVulnerabilities": 0, "closedVulnerabilities": 0}
    if await validate_finding(finding=finding_):
        vulnerabilities = await context.finding_vulns_nzr.load(finding_id)
        last_approved_status = [
            vulns_utils.get_last_status(vuln) for vuln in vulnerabilities
        ]
        for current_state in last_approved_status:
            if current_state == "open":
                finding["openVulnerabilities"] += 1
            elif current_state == "closed":
                finding["closedVulnerabilities"] += 1
            else:
                # Vulnerability does not have a valid state
                pass
    return finding


async def total_vulnerabilities_new(
    loaders: Any, finding: Finding
) -> Dict[str, int]:
    finding_stats = {"openVulnerabilities": 0, "closedVulnerabilities": 0}
    finding_vulns_loader = loaders.finding_vulns_nzr
    if not is_deleted_new(finding):
        vulns = await finding_vulns_loader.load(finding.id)
        last_approved_status = await collect(
            [in_process(vulns_utils.get_last_status, vuln) for vuln in vulns]
        )
        for current_state in last_approved_status:
            if current_state == "open":
                finding_stats["openVulnerabilities"] += 1
            elif current_state == "closed":
                finding_stats["closedVulnerabilities"] += 1
            else:
                # Vulnerability does not have a valid state
                pass
    return finding_stats


async def update_description(
    finding_id: str, updated_values: Dict[str, FindingType]
) -> bool:
    validations.validate_fields(
        list(cast(Dict[str, str], updated_values.values()))
    )
    updated_values["finding"] = updated_values.get("title")
    updated_values["vulnerability"] = updated_values.get("description")
    updated_values["effect_solution"] = updated_values.get("recommendation")
    updated_values["records_number"] = str(
        updated_values.get("records_number")
    )
    updated_values["id"] = finding_id
    del updated_values["title"]
    del updated_values["description"]
    del updated_values["recommendation"]
    updated_values = {
        key: None if not value else value
        for key, value in updated_values.items()
    }
    updated_values = {
        utils.camelcase_to_snakecase(k): updated_values.get(k)
        for k in updated_values
    }

    if findings_utils.is_valid_finding_title(
        str(updated_values.get("finding", ""))
    ):
        return await findings_dal.update(finding_id, updated_values)
    raise InvalidDraftTitle()


async def update_description_new(
    loaders: Any, finding_id: str, description: FindingDescriptionToUpdate
) -> None:
    validations.validate_fields(
        list(filter(None, description._asdict().values()))
    )
    if (
        description.title is not None
        and not findings_utils.is_valid_finding_title(description.title)
    ):
        raise InvalidDraftTitle()

    finding_loader = loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    metadata = FindingMetadataToUpdate(
        actor=description.actor,
        affected_systems=description.affected_systems,
        attack_vector_description=description.attack_vector_description,
        compromised_attributes=description.compromised_attributes,
        compromised_records=description.compromised_records,
        description=description.description,
        recommendation=description.recommendation,
        requirements=description.requirements,
        risk=description.risk,
        scenario=description.sorts,
        sorts=description.sorts,
        threat=description.threat,
        title=description.title,
        type=description.type,
    )
    await findings_model.update_medatada(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def update_severity_new(
    loaders: Any,
    finding_id: str,
    severity: Union[Finding20Severity, Finding31Severity],
) -> None:
    finding_loader = loaders.finding_new
    finding: Finding = await finding_loader.load(finding_id)
    if isinstance(severity, Finding31Severity):
        privileges = cvss.calculate_privileges(
            float(severity.privileges_required),
            float(severity.severity_scope),
        )
        privileges_required = Decimal(privileges).quantize(Decimal("0.01"))
        modified_privileges = cvss.calculate_privileges(
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
    await findings_model.update_medatada(
        group_name=finding.group_name,
        finding_id=finding.id,
        metadata=metadata,
    )


async def validate_finding(
    finding_id: Union[str, int] = 0,
    finding: Optional[Dict[str, FindingType]] = None,
) -> bool:
    """Validate if a finding is not deleted"""
    if not finding:
        non_optional_finding = await findings_dal.get_finding(str(finding_id))
    return not is_deleted(finding or non_optional_finding)


async def verify_vulnerabilities(  # pylint: disable=too-many-locals
    *,
    info: GraphQLResolveInfo,
    finding_id: str,
    user_info: Dict[str, str],
    parameters: Dict[str, FindingType],
    vulns_to_close_from_file: List[Dict[str, str]],
) -> bool:
    # All vulns must be open before verifying them
    # we will just keep them open or close them
    # in either case, their historic_verification is updated to VERIFIED
    finding_vulns_loader = info.context.loaders.finding_vulns_all
    vulnerability_ids: List[str] = get_key_or_fallback(
        parameters, "open_vulnerabilities", "open_vulns", []
    ) + get_key_or_fallback(
        parameters, "closed_vulnerabilities", "closed_vulns", []
    )
    vulnerabilities = [
        vuln
        for vuln in await finding_vulns_loader.load(finding_id)
        if vuln["id"] in vulnerability_ids
    ]
    vulnerabilities = [
        vulns_utils.validate_verify(vuln) for vuln in vulnerabilities
    ]
    vulnerabilities = [
        vulns_utils.validate_closed(vuln) for vuln in vulnerabilities
    ]
    if not vulnerabilities:
        raise VulnNotFound()

    comment_id = str(round(time() * 1000))
    today = datetime_utils.get_now_as_str()
    user_email: str = user_info["user_email"]

    # Modify the verification state to mark the finding as verified
    if FI_API_STATUS == "migration":
        finding_new_loader = info.context.loaders.finding_new
        finding_new: Finding = await finding_new_loader.load(finding_id)
        verification = FindingVerification(
            comment_id=comment_id,
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status=FindingVerificationStatus.VERIFIED,
            vulnerability_ids=vulnerability_ids,
        )
        await findings_model.update_verification(
            group_name=finding_new.group_name,
            finding_id=finding_new.id,
            verification=verification,
        )
        update_finding = True
    else:
        finding_loader = info.context.loaders.finding
        finding = await finding_loader.load(finding_id)
        historic_verification = cast(
            List[Dict[str, Union[str, int, List[str]]]],
            finding.get("historic_verification", []),
        )
        historic_verification.append(
            {
                "comment": comment_id,
                "date": today,
                "status": "VERIFIED",
                "user": user_email,
                "vulns": vulnerability_ids,
            }
        )
        update_finding = await findings_dal.update(
            finding_id, {"historic_verification": historic_verification}
        )
    comment_data = {
        "comment_type": "verification",
        "content": parameters.get("justification", ""),
        "parent": "0",
        "comment_id": comment_id,
    }
    await comments_domain.add(finding_id, comment_data, user_info)

    # Modify the verification state to mark all passed vulns as verified
    success = await collect(
        map(vulns_domain.verify_vulnerability, vulnerabilities)
    )
    if all(success) and update_finding:
        # Open vulns that remain open are not modified in the DB
        # Open vulns that were closed must be persisted to the DB as closed
        success = await vulns_domain.verify(
            info=info,
            finding_id=finding_id,
            vulnerabilities=vulnerabilities,
            closed_vulnerabilities=get_key_or_fallback(
                parameters, "closed_vulnerabilities", "closed_vulns", []
            ),
            date=today,
            vulns_to_close_from_file=vulns_to_close_from_file,
        )
    else:
        LOGGER.error("An error occurred verifying", **NOEXTRA)
    return all(success)


async def get_oldest_no_treatment(
    loaders: Any,
    findings: List[Dict[str, FindingType]],
) -> dict:
    """Get the finding with oldest "new treatment" vuln"""
    finding_vulns_loader = loaders.finding_vulns_nzr
    vulns = await finding_vulns_loader.load_many_chained(
        [str(finding["finding_id"]) for finding in findings]
    )
    new_vulns = [
        {
            **vuln,
            "new_treatment_date": datetime_utils.get_from_str(
                vuln["historic_treatment"][-1]["date"]
            ),
        }
        for vuln in vulns
        if vuln["historic_treatment"][-1]["treatment"] == "NEW"
        and vuln["historic_state"][-1]["state"] == "open"
    ]

    if new_vulns:
        oldest_new_vuln = sorted(
            new_vulns, key=itemgetter("new_treatment_date"), reverse=False
        )[0]
        oldest_finding = next(
            finding
            for finding in findings
            if finding["finding_id"] == oldest_new_vuln["finding_id"]
        )

        return {
            "oldest_name": oldest_finding["title"],
            "oldest_age": (
                datetime_utils.get_now()
                - oldest_new_vuln["new_treatment_date"]
            ).days,
        }

    return dict()


async def get_oldest_no_treatment_new(
    loaders: Any,
    findings: Tuple[Finding, ...],
) -> Dict[str, str]:
    """Get the finding with oldest "new treatment" vuln"""
    finding_vulns_loader = loaders.finding_vulns_nzr
    vulns = await finding_vulns_loader.load_many_chained(
        [str(finding.id) for finding in findings]
    )
    new_vulns = [
        {
            **vuln,
            "new_treatment_date": datetime_utils.get_from_str(
                vuln["historic_treatment"][-1]["date"]
            ),
        }
        for vuln in vulns
        if vuln["historic_treatment"][-1]["treatment"] == "NEW"
        and vuln["historic_state"][-1]["state"] == "open"
    ]

    if new_vulns:
        oldest_new_vuln = sorted(
            new_vulns, key=itemgetter("new_treatment_date"), reverse=False
        )[0]
        oldest_finding: Finding = next(
            finding
            for finding in findings
            if finding.id == oldest_new_vuln["finding_id"]
        )

        return {
            "oldest_name": oldest_finding.title,
            "oldest_age": (
                datetime_utils.get_now()
                - oldest_new_vuln["new_treatment_date"]
            ).days,
        }

    return {}
