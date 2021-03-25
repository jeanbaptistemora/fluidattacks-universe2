# Standard
from typing import cast, Tuple

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Project as Group
from roots.types import Root


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Tuple[Root, ...]:
    group_name: str = cast(str, parent['name'])

    group_roots_loader: DataLoader = info.context.loaders.group_roots
    roots: Tuple[Root, ...] = await group_roots_loader.load(group_name)

    return roots
