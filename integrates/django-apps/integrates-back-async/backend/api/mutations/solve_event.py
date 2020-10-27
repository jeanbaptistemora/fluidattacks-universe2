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
from backend.domain import event as event_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
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
    success = await event_domain.solve_event(
        event_id, affectation, analyst_email, date
    )

    if success:
        event = await event_domain.get_event(event_id)
        project_name = str(event.get('project_name', ''))
        util.queue_cache_invalidation(event_id, project_name)
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
