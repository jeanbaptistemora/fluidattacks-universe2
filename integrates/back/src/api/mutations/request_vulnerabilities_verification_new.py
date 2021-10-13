from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_continuous,
    require_finding_access,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
    List,
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
    require_finding_access,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
    vulnerabilities: List[str],
) -> SimplePayloadType:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        await findings_domain.request_vulnerabilities_verification(
            info.context,
            finding_id,
            user_info,
            justification,
            set(vulnerabilities),
        )
        redis_del_by_deps_soon(
            "request_vulnerabilities_verification",
            finding_id=finding_id,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.request_vulnerabilities_verification,
            finding_id=finding_id,
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
