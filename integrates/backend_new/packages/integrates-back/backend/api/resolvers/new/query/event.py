# Standard
# None

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_integrates,
    require_login,
)
from backend.typing import Event


@rename_kwargs({'identifier': 'event_id'})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
@rename_kwargs({'event_id': 'identifier'})
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Event:
    event_id: str = kwargs['identifier']

    event_loader: DataLoader = info.context.loaders['event']
    event: Event = await event_loader.load(event_id)

    return event
