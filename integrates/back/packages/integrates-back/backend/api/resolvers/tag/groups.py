# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Project as Group, Tag


async def resolve(
    parent: Tag,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    group_names: str = cast(str, parent['projects'])

    group_loader: DataLoader = info.context.loaders['group']
    groups: List[Group] = await group_loader.load_many(group_names)

    return groups
