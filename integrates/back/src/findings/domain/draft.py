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
    validations as validation_utils,
)
from newutils.findings import (
    get_formatted_evidence,
)
from newutils.validations import (
    validate_field_length,
)
from typing import (
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
    group_name: str,
    user_email: str,
    draft_info: FindingDraftToAdd,
    source: Source,
) -> Finding:
    await findings_utils.is_valid_finding_title(draft_info.title)

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


async def reject_draft(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    finding_id: str,
    reasons: set[DraftRejectionReason],
    other: Optional[str],
    reviewer_email: str,
    source: Source,
) -> DraftRejection:
    if other:
        validation_utils.validate_fields([other])
        validation_utils.validate_field_length(
            other,
            limit=5000,
            is_greater_than_limit=False,
        )

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
