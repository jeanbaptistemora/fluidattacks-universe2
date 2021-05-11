
from typing import (
    List,
    cast,
)

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import (
    Event,
    Project as Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
)
from events import domain as events_domain


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Event]:
    group_name: str = cast(str, parent['name'])

    event_ids = await events_domain.list_group_events(group_name)
    event_loader: DataLoader = info.context.loaders.event
    events: List[Event] = await event_loader.load_many(event_ids)

    return events
