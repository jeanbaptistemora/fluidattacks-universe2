from aioextensions import (
    collect,
)
from back.src.machine.availability import (
    operation_can_be_executed,
)
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    InvalidDraftTitle,
    MachineCanNotOperate,
    NotSubmitted,
)
from datetime import (
    datetime,
)
from db_model import (
    findings as findings_model,
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
from findings.types import (
    FindingDraftToAdd,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
    vulnerabilities as vulns_utils,
)
from typing import (
    Any,
    Dict,
)
import uuid
from vulnerabilities import (
    domain as vulns_domain,
)


async def approve_draft(
    context: Any,
    finding_id: str,
    user_email: str,
) -> str:
    finding_all_vulns_loader = context.loaders.finding_vulns_all
    finding_nzr_vulns_loader = context.loaders.finding_vulns_nzr
    finding_loader = context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)

    if not operation_can_be_executed(context, finding.title):
        raise MachineCanNotOperate()

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
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.APPROVED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
    all_vulns = await finding_all_vulns_loader.load(finding_id)
    old_format_approval_date = datetime_utils.get_as_str(
        datetime.fromisoformat(approval_date)
    )
    await collect(
        vulns_domain.update_historics_dates(
            finding_id, vuln, old_format_approval_date
        )
        for vuln in all_vulns
    )
    return approval_date


async def add_draft(
    context: Any,
    group_name: str,
    user_email: str,
    draft_info: FindingDraftToAdd,
) -> None:
    if not findings_utils.is_valid_finding_title(draft_info.title):
        raise InvalidDraftTitle()
    if not operation_can_be_executed(context, draft_info.title):
        raise MachineCanNotOperate()

    group_name = group_name.lower()
    finding_id = str(uuid.uuid4())
    draft = Finding(
        affected_systems=draft_info.affected_systems,
        hacker_email=user_email,
        attack_vector_description=draft_info.attack_vector_description,
        description=draft_info.description,
        group_name=group_name,
        id=finding_id,
        state=FindingState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            source=requests_utils.get_source_new(context),
            status=FindingStateStatus.CREATED,
        ),
        recommendation=draft_info.recommendation,
        requirements=draft_info.requirements,
        severity=draft_info.severity,
        title=draft_info.title,
        threat=draft_info.threat,
    )
    await findings_model.add(finding=draft)


async def reject_draft(context: Any, finding_id: str, user_email: str) -> None:
    finding_loader = context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    new_state = FindingState(
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.REJECTED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )


async def submit_draft(context: Any, finding_id: str, user_email: str) -> None:
    finding_vulns_loader = context.loaders.finding_vulns
    finding_loader = context.loaders.finding
    finding: Finding = await finding_loader.load(finding_id)
    if not operation_can_be_executed(context, finding.title):
        raise MachineCanNotOperate()

    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status == FindingStateStatus.SUBMITTED:
        raise AlreadySubmitted()

    has_severity = findings_domain.get_severity_score(
        finding.severity
    ) > Decimal(0)
    has_vulns = bool(await finding_vulns_loader.load(finding_id))
    if not has_severity or not has_vulns:
        required_fields: Dict[str, bool] = {
            "severity": has_severity,
            "vulnerabilities": has_vulns,
        }
        raise IncompleteDraft(
            [key for key, value in required_fields.items() if not value]
        )

    new_state = FindingState(
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.SUBMITTED,
    )
    await findings_model.update_state(
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
