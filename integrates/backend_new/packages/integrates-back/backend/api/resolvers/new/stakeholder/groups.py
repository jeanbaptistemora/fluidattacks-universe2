# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from aioextensions import collect
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import user as user_domain
from backend.typing import Project as Group, Stakeholder


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Group]:
    email: str = cast(str, parent['email'])

    active, inactive = await collect([
        user_domain.get_projects(email),
        user_domain.get_projects(email, active=False)
    ])
    user_groups: List[str] = active + inactive

    group_loader: DataLoader = info.context.loaders['group']
    groups: List[Group] = await group_loader.load_many(user_groups)

    return groups
