# Standard
from functools import (
    partial,
)
from typing import cast

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.decorators import require_integrates
from backend.typing import Project as Group


@require_integrates
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, _info, **_kwargs),
        entity='group',
        attr='total_findings',
        name=cast(str, parent['name']),
    )

    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    group_name: str = cast(str, parent['name'])
    group_findings_loader: DataLoader = info.context.loaders.group_findings

    return len(await group_findings_loader.load(group_name))
