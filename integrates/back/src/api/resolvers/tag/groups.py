from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Project as Group,
    Tag,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
    List,
)


async def resolve(
    parent: Tag, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Group]:
    group_names: str = cast(str, parent["projects"])
    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(group_names)

    return groups
