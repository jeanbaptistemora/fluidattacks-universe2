from aiodataloader import (
    DataLoader,
)
from db_model.toe_lines.types import (
    ServicesToeLines,
)
from decorators import (
    enforce_group_level_auth_async,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from roots.types import (
    GitRoot,
)
from typing import (
    Tuple,
)

# Constants
CACHE_TTL = 60 * 30


@enforce_group_level_auth_async
async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo, **kwargs: None
) -> Tuple[ServicesToeLines, ...]:
    response: Tuple[
        ServicesToeLines, ...
    ] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="root",
        attr="toe_lines",
        ttl=CACHE_TTL,
        group=parent.group_name,
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: GitRoot, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[ServicesToeLines, ...]:
    group_name = parent.group_name
    root_id = parent.id
    root_toe_lines_loader: DataLoader = info.context.loaders.root_toe_lines
    root_toe_lines = await root_toe_lines_loader.load((group_name, root_id))

    return root_toe_lines
