from aiodataloader import (
    DataLoader,
)
from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
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
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.validations import (
    validate_no_duplicate_drafts,
)
from typing import (
    Any,
    Tuple,
)


@convert_kwargs_to_snake_case
@rename_kwargs({"project_name": "group_name"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    title: str,
    **kwargs: Any,
) -> SimplePayload:
    # Duplicate check
    group_findings_loader: DataLoader = info.context.loaders.group_findings
    group_drafts_loader: DataLoader = info.context.loaders.group_drafts
    drafts: Tuple[Finding, ...] = await group_drafts_loader.load(group_name)
    findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    validate_no_duplicate_drafts(title, drafts, findings)

    try:
        user_info = await token_utils.get_jwt_content(info.context)
        user_email = user_info["user_email"]
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
            affected_systems=kwargs.get("affected_systems", ""),
            attack_vector_description=kwargs.get(
                "attack_vector_description", ""
            )
            or kwargs.get("attack_vector_desc", ""),
            description=kwargs.get("description", ""),
            hacker_email=user_email,
            recommendation=kwargs.get("recommendation", ""),
            requirements=kwargs.get("requirements", ""),
            severity=severity_info,
            threat=kwargs.get("threat", ""),
            title=title,
        )
        await findings_domain.add_draft(
            info.context, group_name, user_email, draft_info
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
    return SimplePayload(success=True)
