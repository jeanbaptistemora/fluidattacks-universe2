from .core import (
    get_finding,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    NotSubmitted,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    DraftRejectionReason,
    FindingStateStatus,
)
from db_model.findings.types import (
    DraftRejection,
    Finding,
    Finding31Severity,
    FindingState,
)
from db_model.utils import (
    get_datetime_with_offset,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDraftToAdd,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
)
from newutils.findings import (
    get_formatted_evidence,
)
from newutils.validations import (
    check_and_set_min_time_to_remediate,
    validate_all_fields_length_deco,
    validate_field_length,
    validate_field_length_deco,
    validate_fields_deco,
    validate_no_duplicate_drafts_deco,
)
from typing import (
    Any,
    Optional,
)
import uuid
from vulnerabilities import (
    domain as vulns_domain,
)


async def approve_draft(
    loaders: Dataloaders,
    finding_id: str,
    user_email: str,
    source: Source,
) -> datetime:
    finding = await get_finding(loaders, finding_id)

    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    nzr_vulns = await loaders.finding_vulnerabilities_released_nzr.load(
        finding_id
    )
    if not nzr_vulns:
        raise DraftWithoutVulns()
    has_evidence = any(
        bool(evidence["url"])
        for evidence in get_formatted_evidence(finding).values()
    )
    if not has_evidence:
        required_fields: dict[str, bool] = {
            "evidences": has_evidence,
        }
        raise IncompleteDraft(
            [key for key, value in required_fields.items() if not value]
        )

    new_state = FindingState(
        modified_by=user_email,
        modified_date=get_datetime_with_offset(
            finding.state.modified_date, datetime_utils.get_utc_now()
        ),
        source=source,
        status=FindingStateStatus.APPROVED,
    )
    await collect(
        (
            findings_model.update_state(
                current_value=finding.state,
                finding_id=finding.id,
                group_name=finding.group_name,
                state=new_state,
            ),
            findings_model.update_me_draft_index(
                finding_id=finding.id,
                group_name=finding.group_name,
                user_email="",
            ),
        )
    )
    finding_vulnerabilities = await loaders.finding_vulnerabilities_all.load(
        finding_id
    )
    await collect(
        vulns_domain.update_historics_dates(
            loaders=loaders,
            finding_id=finding_id,
            vulnerability_id=vuln.id,
            modified_date=new_state.modified_date,
        )
        for vuln in finding_vulnerabilities
    )

    return new_state.modified_date


def validate_draft_inputs(*, kwargs: list[str]) -> None:
    for value in kwargs:
        if isinstance(value, str):
            validate_field_length(value, 5000)


async def add_draft(
    loaders: Dataloaders,
    group_name: str,
    user_email: str,
    draft_info: FindingDraftToAdd,
    source: Source,
) -> Finding:
    await findings_utils.is_valid_finding_title(loaders, draft_info.title)

    group_name = group_name.lower()
    finding_id = str(uuid.uuid4())
    draft = Finding(
        hacker_email=user_email,
        attack_vector_description=draft_info.attack_vector_description,
        description=draft_info.description,
        group_name=group_name,
        id=finding_id,
        min_time_to_remediate=draft_info.min_time_to_remediate,
        state=FindingState(
            modified_by=user_email,
            modified_date=datetime_utils.get_utc_now(),
            source=source,
            status=FindingStateStatus.CREATED,
        ),
        recommendation=draft_info.recommendation,
        requirements=draft_info.requirements,
        severity=draft_info.severity,
        title=draft_info.title,
        threat=draft_info.threat,
    )
    await findings_model.add(finding=draft)
    return draft


@validate_fields_deco(["other"])
@validate_field_length_deco("other", limit=5000, is_greater_than_limit=False)
async def reject_draft(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    reasons: set[DraftRejectionReason],
    other: Optional[str],
    reviewer_email: str,
    source: Source,
) -> DraftRejection:
    finding = await get_finding(loaders, finding_id)
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()
    if DraftRejectionReason.OTHER in reasons and not other:
        raise IncompleteDraft(fields=["other"])

    rejection_date = get_datetime_with_offset(
        finding.state.modified_date, datetime_utils.get_utc_now()
    )
    rejection = DraftRejection(
        other=other if other else "",
        reasons=reasons,
        rejected_by=reviewer_email,
        rejection_date=rejection_date,
        submitted_by=finding.state.modified_by,
    )
    new_state = FindingState(
        modified_by=reviewer_email,
        modified_date=rejection_date,
        rejection=rejection,
        source=source,
        status=FindingStateStatus.REJECTED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
    return rejection


async def submit_draft(
    loaders: Dataloaders,
    finding_id: str,
    user_email: str,
    source: Source,
) -> None:
    finding = await get_finding(loaders, finding_id)

    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status == FindingStateStatus.SUBMITTED:
        raise AlreadySubmitted()

    has_severity = findings_domain.get_severity_score(
        finding.severity
    ) > Decimal(0)
    has_vulns = bool(
        await loaders.finding_vulnerabilities_released_nzr.load(finding_id)
    )
    has_evidence = any(
        bool(evidence["url"])
        for evidence in get_formatted_evidence(finding).values()
    )
    if not has_severity or not has_vulns or not has_evidence:
        required_fields: dict[str, bool] = {
            "evidences": has_evidence,
            "severity": has_severity,
            "vulnerabilities": has_vulns,
        }
        raise IncompleteDraft(
            [key for key, value in required_fields.items() if not value]
        )

    new_state = FindingState(
        modified_by=user_email,
        modified_date=get_datetime_with_offset(
            finding.state.modified_date, datetime_utils.get_utc_now()
        ),
        source=source,
        status=FindingStateStatus.SUBMITTED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )


@validate_no_duplicate_drafts_deco("title", "drafts", "findings")
@validate_fields_deco(
    [
        "attack_vector_description",
        "description",
        "recommendation",
        "requirements",
        "threat",
    ]
)
@validate_all_fields_length_deco(limit=5000)
def get_draft_info(
    user_email: str, title: str, **kwargs: Any
) -> FindingDraftToAdd:
    min_time_to_remediate = check_and_set_min_time_to_remediate(
        kwargs.get("min_time_to_remediate", None)
    )
    severity_info = Finding31Severity(
        attack_complexity=Decimal(kwargs.get("attack_complexity", "0.0")),
        attack_vector=Decimal(kwargs.get("attack_vector", "0.0")),
        availability_impact=Decimal(kwargs.get("availability_impact", "0.0")),
        confidentiality_impact=Decimal(
            kwargs.get("confidentiality_impact", "0.0")
        ),
        exploitability=Decimal(kwargs.get("exploitability", "0.0")),
        integrity_impact=Decimal(kwargs.get("integrity_impact", "0.0")),
        privileges_required=Decimal(kwargs.get("privileges_required", "0.0")),
        remediation_level=Decimal(kwargs.get("remediation_level", "0.0")),
        report_confidence=Decimal(kwargs.get("report_confidence", "0.0")),
        severity_scope=Decimal(kwargs.get("severity_scope", "0.0")),
        user_interaction=Decimal(kwargs.get("user_interaction", "0.0")),
    )
    draft_info = FindingDraftToAdd(
        attack_vector_description=kwargs.get("attack_vector_description", "")
        or kwargs.get("attack_vector_desc", ""),
        description=kwargs.get("description", ""),
        hacker_email=user_email,
        min_time_to_remediate=min_time_to_remediate,
        recommendation=kwargs.get("recommendation", ""),
        requirements=kwargs.get("requirements", ""),
        severity=severity_info,
        threat=kwargs.get("threat", ""),
        title=title,
    )
    return draft_info
