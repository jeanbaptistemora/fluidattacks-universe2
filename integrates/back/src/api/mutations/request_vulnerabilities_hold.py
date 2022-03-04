from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    EventAlreadyClosed,
    EventNotFound,
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
    group_name: str,
    finding_id: str,
    vulnerabilities: List[str],
) -> SimplePayloadType:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        event_loader = info.context.loaders.event
        event = await event_loader.load(event_id)
        if "group_name" not in event or group_name != event["group_name"]:
            raise EventNotFound()
        if event["event_status"].upper() == "SOLVED":
            raise EventAlreadyClosed()

        await events_domain.request_vulnerabilities_hold(
            loaders=info.context.loaders,
            event_id=event_id,
            finding_id=finding_id,
            user_info=user_info,
            vulnerability_ids=set(vulnerabilities),
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
