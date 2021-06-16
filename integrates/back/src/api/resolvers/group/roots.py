from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    Root,
)
from typing import (
    cast,
    Tuple,
)


async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Root, ...]:
    group_name: str = cast(str, parent["name"])
    group_roots_loader: DataLoader = info.context.loaders.group_roots
    roots: Tuple[Root, ...] = await group_roots_loader.load(group_name)
    return roots
