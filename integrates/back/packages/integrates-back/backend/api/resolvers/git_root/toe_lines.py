# Standard
from functools import (
    partial,
)
from typing import Tuple

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from data_containers.toe_lines import GitRootToeLines
from roots.types import GitRoot

# Constants
CACHE_TTL = 60 * 30


async def resolve(
    parent: GitRoot,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> Tuple[GitRootToeLines, ...]:
    response: Tuple[GitRootToeLines, ...] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='toe_lines',
        name=parent.group_name
    )

    return response


async def resolve_no_cache(
    parent: GitRoot,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Tuple[GitRootToeLines, ...]:
    group_name = parent.group_name
    root_id = parent.id
    root_toe_lines_loader: DataLoader = info.context.loaders.root_toe_lines
    root_toe_lines = await root_toe_lines_loader.load((group_name, root_id))

    return root_toe_lines
