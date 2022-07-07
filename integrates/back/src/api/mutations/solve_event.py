from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.events.enums import (
    EventSolutionReason,
)
from db_model.events.types import (
    Event,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
    Optional,
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
    reason: str,
    other: Optional[str],
    **_kwargs: Any,
) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    hacker_email = user_info["user_email"]
    (reattacks_dict, verifications_dict,) = await events_domain.solve_event(
        info, event_id, hacker_email, EventSolutionReason[reason], other
    )

    loaders: Dataloaders = info.context.loaders
    loaders.event.clear(event_id)
    event: Event = await loaders.event.load(event_id)
    group_name = event.group_name
    redis_del_by_deps_soon("solve_event", group_name=group_name)
    logs_utils.cloudwatch_log(
        info.context, f"Security: Solved event {event_id} successfully"
    )
    await update_unreliable_indicators_by_deps(
        EntityDependency.solve_event,
        event_ids=[event_id],
    )
    if bool(reattacks_dict):
        await update_unreliable_indicators_by_deps(
            EntityDependency.request_vulnerabilities_verification,
            finding_ids=list(reattacks_dict.keys()),
            vulnerability_ids=[
                vuln_id
                for reattack_ids in reattacks_dict.values()
                for vuln_id in reattack_ids
            ],
        )
    if bool(verifications_dict):
        await update_unreliable_indicators_by_deps(
            EntityDependency.verify_vulnerabilities_request,
            finding_ids=list(verifications_dict.keys()),
            vulnerability_ids=[
                vuln_id
                for verification_ids in verifications_dict.values()
                for vuln_id in verification_ids
            ],
        )
    else:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to solve event {event_id}"
        )

    return SimplePayload(success=True)
