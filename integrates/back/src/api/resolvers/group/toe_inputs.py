from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from db_model.toe_inputs.types import (
    ToeInput,
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
from typing import (
    Tuple,
)

# Constants
CACHE_TTL = 60 * 30


@enforce_group_level_auth_async
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **kwargs: None
) -> Tuple[ToeInput, ...]:
    response: Tuple[ToeInput, ...] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="toe_inputs",
        ttl=CACHE_TTL,
        name=parent["name"],
    )
    return response


async def resolve_no_cache(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[ToeInput, ...]:
    group_name: str = parent["name"]
    group_toe_inputs_loader: DataLoader = info.context.loaders.group_toe_inputs
    group_toe_inputs: Tuple[
        ToeInput, ...
    ] = await group_toe_inputs_loader.load(group_name)
    return group_toe_inputs
