# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.domain import project as group_domain
from backend.typing import Event, Project as Group


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Event]:
    group_name: str = cast(str, parent['project_name'])

    event_ids = await group_domain.list_events(group_name)
    event_loader: DataLoader = info.context.loaders['event']
    events: List[Event] = await event_loader.load_many(event_ids)

    return events
