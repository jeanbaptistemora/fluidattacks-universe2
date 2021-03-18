# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Project as Group, Stakeholder
from users import domain as users_domain


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    email: str = cast(str, parent['email'])

    active, inactive = await collect([
        users_domain.get_projects(email),
        users_domain.get_projects(email, active=False)
    ])
    user_groups: List[str] = active + inactive

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(user_groups)

    return groups
