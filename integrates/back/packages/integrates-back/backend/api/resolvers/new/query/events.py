# Standard
from typing import List

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.domain import project as group_domain
from backend.typing import Event


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Event]:
    group_name: str = kwargs['project_name']

    event_ids = await group_domain.list_events(group_name.lower())
    event_loader: DataLoader = info.context.loaders['event']
    events: List[Event] = await event_loader.load_many(event_ids)

    return events
