from .payloads.types import (
    SimplePayload,
)
from api.types import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    MachineCanNotOperate,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding31Severity,
)
from decimal import (
    Decimal,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingAttributesToAdd,
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
)
from newutils.validations import (
    check_and_set_min_time_to_remediate,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
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
    description: str,
    recommendation: str,
    title: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    stakeholder_info = await sessions_domain.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    try:
        if not operation_can_be_executed(info.context, title):
            raise MachineCanNotOperate()

        await findings_domain.add_finding(
            loaders=loaders,
            group_name=group_name,
            stakeholder_email=stakeholder_email,
            attributes=FindingAttributesToAdd(
                attack_vector_description=kwargs.get(
                    "attack_vector_description", ""
                ),
                description=description,
                min_time_to_remediate=check_and_set_min_time_to_remediate(
                    kwargs.get("min_time_to_remediate", None)
                ),
                recommendation=recommendation,
                severity=Finding31Severity(
                    attack_complexity=Decimal(
                        kwargs.get("attack_complexity", "0.0")
                    ),
                    attack_vector=Decimal(kwargs.get("attack_vector", "0.0")),
                    availability_impact=Decimal(
                        kwargs.get("availability_impact", "0.0")
                    ),
                    confidentiality_impact=Decimal(
                        kwargs.get("confidentiality_impact", "0.0")
                    ),
                    exploitability=Decimal(
                        kwargs.get("exploitability", "0.0")
                    ),
                    integrity_impact=Decimal(
                        kwargs.get("integrity_impact", "0.0")
                    ),
                    privileges_required=Decimal(
                        kwargs.get("privileges_required", "0.0")
                    ),
                    remediation_level=Decimal(
                        kwargs.get("remediation_level", "0.0")
                    ),
                    report_confidence=Decimal(
                        kwargs.get("report_confidence", "0.0")
                    ),
                    severity_scope=Decimal(
                        kwargs.get("severity_scope", "0.0")
                    ),
                    user_interaction=Decimal(
                        kwargs.get("user_interaction", "0.0")
                    ),
                ),
                source=requests_utils.get_source_new(info.context),
                threat=kwargs.get("threat", ""),
                title=title,
                unfulfilled_requirements=kwargs["unfulfilled_requirements"],
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added finding in {group_name} group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add finding in {group_name} group",
        )
        raise

    return SimplePayload(success=True)
