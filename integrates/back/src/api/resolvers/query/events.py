from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
    Dict,
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
) -> List[Dict[str, Any]]:
    # Compatibility with old API
    group_name: str = get_key_or_fallback(kwargs).lower()
    event_ids = await events_domain.list_group_events(group_name.lower())
    event_loader: DataLoader = info.context.loaders.event
    events: List[Dict[str, Any]] = await event_loader.load_many(event_ids)

    return events
