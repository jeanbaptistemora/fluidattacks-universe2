from aioextensions import (
    collect,
)
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    InvalidDraftTitle,
    NotSubmitted,
)
from datetime import (
    datetime,
)
from db_model import (
    findings,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    FindingState,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
    vulnerabilities as vulns_utils,
)
import random
from typing import (
    Any,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def approve_draft_new(
    context: Any,
    finding_id: str,
    group_name: str,
    user_email: str,
) -> str:
    finding_all_vulns_loader = context.loaders.finding_vulns_all
    finding_nzr_vulns_loader = context.loaders.finding_vulns_nzr
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load((group_name, finding_id))
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    nzr_vulns = await finding_nzr_vulns_loader.load(finding_id)
    has_vulns = bool(
        [vuln for vuln in nzr_vulns if vulns_utils.filter_deleted_status(vuln)]
    )
    if not has_vulns:
        raise DraftWithoutVulns()

    approval_date = datetime_utils.get_iso_date()
    new_state = FindingState(
        modified_by=user_email,
        modified_date=approval_date,
        source=requests_utils.get_source(context),
        status=FindingStateStatus.APPROVED,
    )
    await findings.update_state(
        finding_id=finding_id,
        group_name=group_name,
        state=new_state,
    )
    all_vulns = await finding_all_vulns_loader.load(finding_id)
    old_format_approval_date = datetime_utils.get_as_str(
        datetime.fromisoformat(approval_date)
    )
    await collect(
        vulns_domain.update_historic_state_dates(
            finding_id, vuln, old_format_approval_date
        )
        for vuln in all_vulns
    )
    return approval_date


async def create_draft_new(
    context: Any, group_name: str, title: str, user_email: str, **kwargs: Any
) -> None:
    if not findings_utils.is_valid_finding_title(title):
        raise InvalidDraftTitle()

    group_name = group_name.lower()
    last_fs_id = 550000000
    finding_id = str(random.randint(last_fs_id, 1000000000))
    draft = Finding(
        affected_systems=kwargs.get("affected_systems", ""),
        analyst_email=user_email,
        attack_vector_desc=kwargs.get("attack_vector_desc", ""),
        cwe=kwargs.get("cwe", ""),
        description=kwargs.get("description", ""),
        group_name=group_name,
        id=finding_id,
        state=FindingState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            source=requests_utils.get_source(context),
            status=FindingStateStatus.CREATED,
        ),
        risk=kwargs.get("risk", ""),
        recommendation=kwargs.get("recommendation", ""),
        requirements=kwargs.get("requirements", ""),
        title=title,
        threat=kwargs.get("threat", ""),
        type=kwargs.get("type", ""),
    )
    await findings.create(finding=draft)


async def reject_draft_new(
    context: Any, finding_id: str, group_name: str, user_email: str
) -> None:
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load((group_name, finding_id))
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    new_state = FindingState(
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source(context),
        status=FindingStateStatus.REJECTED,
    )
    await findings.update_state(
        finding_id=finding_id,
        group_name=group_name,
        state=new_state,
    )


async def submit_draft_new(
    context: Any, finding_id: str, group_name: str, user_email: str
) -> None:
    finding_vulns_loader = context.loaders.finding_vulns
    finding_loader = context.loaders.finding_new
    finding: Finding = await finding_loader.load((group_name, finding_id))
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status == FindingStateStatus.SUBMITTED:
        raise AlreadySubmitted()

    has_severity = findings_domain.get_severity_score_new(
        finding.severity
    ) > Decimal(0)
    has_vulns = bool(await finding_vulns_loader.load(finding_id))
    if not has_severity or not has_vulns:
        required_fields = {
            "severity": has_severity,
            "vulnerabilities": has_vulns,
        }
        raise IncompleteDraft(
            [field for field in required_fields if not required_fields[field]]
        )

    new_state = FindingState(
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source(context),
        status=FindingStateStatus.SUBMITTED,
    )
    await findings.update_state(
        finding_id=finding_id,
        group_name=group_name,
        state=new_state,
    )
