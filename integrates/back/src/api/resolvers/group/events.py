from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Event,
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Event]:
    group_name: str = parent["name"]

    event_ids = await events_domain.list_group_events(group_name)
    event_loader: DataLoader = info.context.loaders.event
    events: List[Event] = await event_loader.load_many(event_ids)

    return events
