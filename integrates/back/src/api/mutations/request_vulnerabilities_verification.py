from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_continuous,
    require_finding_access,
    require_login,
    require_report_vulnerabilities,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_continuous,
    require_asm,
    require_report_vulnerabilities,
    require_finding_access,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vulnerabilities: list[str],
) -> SimplePayloadType:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)

        await findings_domain.request_vulnerabilities_verification(
            loaders=info.context.loaders,
            finding_id=finding_id,
            user_info=user_info,
            justification=justification,
            vulnerability_ids=set(vulnerabilities),
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.request_vulnerabilities_verification,
            finding_ids=[finding_id],
            vulnerability_ids=vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Request vuln verification in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to request vuln verification in finding "
            f"{finding_id}",
        )
        raise

    return SimplePayloadType(success=True)
