from aioextensions import (
    collect,
)
from custom_exceptions import (
    AlreadyApproved,
    AlreadySubmitted,
    DraftWithoutVulns,
    IncompleteDraft,
    MachineCanNotOperate,
    NotSubmitted,
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
from machine.availability import (
    operation_can_be_executed,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    requests as requests_utils,
)
from newutils.validations import (
    validate_field_length,
)
from typing import (
    Any,
    Dict,
    List,
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
    loaders = context.loaders
    finding: Finding = await loaders.finding.load(finding_id)

    if not operation_can_be_executed(context, finding.title):
        raise MachineCanNotOperate()

    if finding.state.status == FindingStateStatus.APPROVED:
        raise AlreadyApproved()

    if finding.state.status != FindingStateStatus.SUBMITTED:
        raise NotSubmitted()

    nzr_vulns = await loaders.finding_vulns_nzr_typed.load(finding_id)
    if not nzr_vulns:
        raise DraftWithoutVulns()

    approval_date = datetime_utils.get_iso_date_no_fractional()
    new_state = FindingState(
        modified_by=user_email,
        modified_date=approval_date,
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.APPROVED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
    await collect(
        vulns_domain.update_historics_dates(
            loaders=loaders,
            finding_id=finding_id,
            vulnerability_id=vuln.id,
            modified_date=approval_date,
        )
        for vuln in await loaders.finding_vulns_all_typed.load(finding_id)
    )
    return approval_date


def validate_draft_inputs(*, kwargs: List[str]) -> None:
    for value in kwargs:
        if isinstance(value, str):
            validate_field_length(value, 5000)


async def add_draft(
    context: Any,
    group_name: str,
    user_email: str,
    draft_info: FindingDraftToAdd,
) -> None:
    findings_utils.is_valid_finding_title(draft_info.title)
    if not operation_can_be_executed(context, draft_info.title):
        raise MachineCanNotOperate()

    group_name = group_name.lower()
    finding_id = str(uuid.uuid4())
    draft = Finding(
        hacker_email=user_email,
        attack_vector_description=draft_info.attack_vector_description,
        description=draft_info.description,
        group_name=group_name,
        id=finding_id,
        state=FindingState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date_no_fractional(),
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
        modified_date=datetime_utils.get_iso_date_no_fractional(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.REJECTED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )


async def submit_draft(
    context: Any,
    finding_id: str,
    user_email: str,
) -> None:
    finding_vulns_loader = context.loaders.finding_vulns_nzr_typed
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
        modified_date=datetime_utils.get_iso_date_no_fractional(),
        source=requests_utils.get_source_new(context),
        status=FindingStateStatus.SUBMITTED,
    )
    await findings_model.update_state(
        current_value=finding.state,
        finding_id=finding.id,
        group_name=finding.group_name,
        state=new_state,
    )
