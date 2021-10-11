from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Group,
)
from db_model.roots.types import (
    RootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    domain as roots_domain,
)
from roots.types import (
    Root,
)
from typing import (
    Tuple,
)


async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Root, ...]:
    group_name: str = parent["name"]
    group_roots_loader: DataLoader = info.context.loaders.group_roots
    roots: Tuple[RootItem, ...] = await group_roots_loader.load(group_name)

    return tuple(roots_domain.format_root(root) for root in roots)
