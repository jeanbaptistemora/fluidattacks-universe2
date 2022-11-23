from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> List[Event]:
    # Compatibility with old API
    group_name: str = get_key_or_fallback(kwargs).lower()
    event_groups = await info.context.loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )

    return event_groups
