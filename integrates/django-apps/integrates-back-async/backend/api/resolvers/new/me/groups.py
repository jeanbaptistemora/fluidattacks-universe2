# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import user as user_domain
from backend.typing import Me, Project as Group


async def resolve(
    parent: Me,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    user_email: str = cast(str, parent['user_email'])
    user_groups: List[str] = await user_domain.get_projects(user_email)

    group_loader: DataLoader = info.context.loaders['group']
    groups: List[Group] = await group_loader.load_many(user_groups)

    return groups
