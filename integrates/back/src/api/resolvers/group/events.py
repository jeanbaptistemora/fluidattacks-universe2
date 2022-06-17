from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
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
    Any,
    Dict,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    event_ids = await events_domain.list_group_events(group_name)
    events: list[Dict[str, Any]] = await loaders.event_typed.load_many(
        event_ids
    )

    return events
