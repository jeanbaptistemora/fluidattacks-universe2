
from functools import partial
from typing import Tuple

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Project as Group
from data_containers.toe_inputs import GitRootToeInput
from decorators import enforce_group_level_auth_async
from redis_cluster.operations import redis_get_or_set_entity_attr


# Constants
CACHE_TTL = 60 * 30


@enforce_group_level_auth_async
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> Tuple[GitRootToeInput, ...]:
    response: Tuple[GitRootToeInput, ...] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='toe_inputs',
        ttl=CACHE_TTL,
        name=parent['name']
    )
    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Tuple[GitRootToeInput, ...]:
    group_name: str = parent['name']
    group_toe_inputs_loader: DataLoader = info.context.loaders.group_toe_inputs
    group_toe_inputs: Tuple[GitRootToeInput, ...] = (
        await group_toe_inputs_loader.load(group_name)
    )
    return group_toe_inputs
