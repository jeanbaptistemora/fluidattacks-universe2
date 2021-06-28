from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Event,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    resolve_kwargs,
)
from typing import (
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> List[Event]:
    # Compatibility with old API
    group_name: str = resolve_kwargs(kwargs).lower()
    event_ids = await events_domain.list_group_events(group_name.lower())
    event_loader: DataLoader = info.context.loaders.event
    events: List[Event] = await event_loader.load_many(event_ids)

    return events
