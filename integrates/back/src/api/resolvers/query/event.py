from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@rename_kwargs({"identifier": "event_id"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
@rename_kwargs({"event_id": "identifier"})
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Event:
    event_id: str = kwargs["identifier"]
    loaders: Dataloaders = info.context.loaders

    return await events_domain.get_event(loaders, event_id)
