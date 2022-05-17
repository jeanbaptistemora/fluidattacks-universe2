from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from datetime import (
    datetime,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
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
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
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
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    affectation: str,
    date: datetime,
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    hacker_email = user_info["user_email"]
    (success, reattacks_dict) = await events_domain.solve_event(
        info, event_id, affectation, hacker_email, date
    )

    if success:
        info.context.loaders.event.clear(event_id)
        event = await events_domain.get_event(event_id)
        group_name = str(get_key_or_fallback(event, fallback=""))
        redis_del_by_deps_soon("solve_event", group_name=group_name)
        logs_utils.cloudwatch_log(
            info.context, f"Security: Solved event {event_id} successfully"
        )
        if bool(reattacks_dict):
            await update_unreliable_indicators_by_deps(
                EntityDependency.request_vulnerabilities_verification,
                finding_ids=list(reattacks_dict.keys()),
                vulnerability_ids=[
                    vuln_id
                    for hold_ids in reattacks_dict.values()
                    for vuln_id in hold_ids
                ],
            )
    else:
        logs_utils.cloudwatch_log(
            info.context, "Security: Attempted to solve event {event_id}"
        )

    return SimplePayload(success=success)
