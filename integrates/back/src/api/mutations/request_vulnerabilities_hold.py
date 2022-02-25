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
from events import (
    domain as events_domain,
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
    event_id: str,
    finding_id: str,
    vulnerabilities: List[str],
) -> SimplePayloadType:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        justification: str = (
            "These reattacks were put on hold because of " f"Event {event_id}"
        )

        await events_domain.request_vulnerabilities_hold(
            info.context.loaders,
            finding_id,
            user_info,
            justification,
            set(vulnerabilities),
        )
        redis_del_by_deps_soon(
            "request_vulnerabilities_hold",
            event_id=event_id,
        )
        await update_unreliable_indicators_by_deps(
            EntityDependency.request_vulnerabilities_hold,
            finding_ids=[finding_id],
            vulnerability_ids=vulnerabilities,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Requested vuln reattack hold in finding {finding_id}",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to request reattack hold in finding "
            f"{finding_id}",
        )
        raise
    return SimplePayloadType(success=True)
