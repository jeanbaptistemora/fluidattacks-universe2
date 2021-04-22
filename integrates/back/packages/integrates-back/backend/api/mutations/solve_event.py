# Standard
from datetime import datetime

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import SimplePayload
from events import domain as events_domain
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    affectation: str,
    date: datetime
) -> SimplePayload:
    user_info = await util.get_jwt_content(info.context)
    analyst_email = user_info['user_email']
    success = await events_domain.solve_event(
        event_id, affectation, analyst_email, date
    )

    if success:
        info.context.loaders.event.clear(event_id)
        event = await events_domain.get_event(event_id)
        project_name = str(event.get('project_name', ''))
        redis_del_by_deps_soon('solve_event', group_name=project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Solved event {event_id} successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            'Security: Attempted to solve event {event_id}'
        )

    return SimplePayload(success=success)
