from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    AddDraftPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    HasRejectedDrafts,
    MachineCanNotOperate,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from db_model.findings.utils import (
    filter_non_state_status_findings,
    has_rejected_drafts,
)
from decimal import (
    Decimal,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDraftToAdd,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.availability import (
    operation_can_be_executed,
)
from newutils import (
    logs as logs_utils,
    requests as requests_utils,
    token as token_utils,
    validations,
)
from newutils.requests import (
    get_source_new,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@rename_kwargs({"project_name": "group_name"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_report_vulnerabilities,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    title: str,
    **kwargs: Any,
) -> AddDraftPayload:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    if get_source_new(info.context).value != Source.MACHINE.value:
        # Non rejected check
        user_drafts: tuple[
            Finding, ...
        ] = await info.context.loaders.me_drafts.load(user_email)

        if has_rejected_drafts(drafts=user_drafts):
            raise HasRejectedDrafts()

    try:
        # Duplicate check
        drafts_and_findings: tuple[
            Finding, ...
        ] = await info.context.loaders.group_drafts_and_findings.load(
            group_name
        )
        drafts: tuple[Finding, ...] = filter_non_state_status_findings(
            drafts_and_findings,
            {
                FindingStateStatus.APPROVED,
                FindingStateStatus.DELETED,
            },
        )
        findings: tuple[Finding, ...] = filter_non_state_status_findings(
            drafts_and_findings,
            {
                FindingStateStatus.CREATED,
                FindingStateStatus.DELETED,
                FindingStateStatus.REJECTED,
                FindingStateStatus.SUBMITTED,
            },
        )
        validations.validate_no_duplicate_drafts(title, drafts, findings)

        validations.validate_fields(
            [
                kwargs.get("attack_vector_description", ""),
                kwargs.get("description", ""),
                kwargs.get("recommendation", ""),
                kwargs.get("requirements", ""),
                kwargs.get("threat", ""),
            ]
        )
        findings_domain.validate_draft_inputs(kwargs=list(kwargs.values()))
        min_time_to_remediate = (
            validations.check_and_set_min_time_to_remediate(
                kwargs.get("min_time_to_remediate", None)
            )
        )

        severity_info = Finding31Severity(
            attack_complexity=Decimal(kwargs.get("attack_complexity", "0.0")),
            attack_vector=Decimal(kwargs.get("attack_vector", "0.0")),
            availability_impact=Decimal(
                kwargs.get("availability_impact", "0.0")
            ),
            confidentiality_impact=Decimal(
                kwargs.get("confidentiality_impact", "0.0")
            ),
            exploitability=Decimal(kwargs.get("exploitability", "0.0")),
            integrity_impact=Decimal(kwargs.get("integrity_impact", "0.0")),
            privileges_required=Decimal(
                kwargs.get("privileges_required", "0.0")
            ),
            remediation_level=Decimal(kwargs.get("remediation_level", "0.0")),
            report_confidence=Decimal(kwargs.get("report_confidence", "0.0")),
            severity_scope=Decimal(kwargs.get("severity_scope", "0.0")),
            user_interaction=Decimal(kwargs.get("user_interaction", "0.0")),
        )
        draft_info = FindingDraftToAdd(
            attack_vector_description=kwargs.get(
                "attack_vector_description", ""
            )
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
        if not operation_can_be_executed(info.context, draft_info.title):
            raise MachineCanNotOperate()

        draft = await findings_domain.add_draft(
            group_name,
            user_email,
            draft_info,
            source=requests_utils.get_source_new(info.context),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created draft in {group_name} group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to create draft in {group_name} group",
        )
        raise
    return AddDraftPayload(draft_id=draft.id, success=True)
