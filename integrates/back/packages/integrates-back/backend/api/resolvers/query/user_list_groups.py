# Standard
from typing import List

# Third party
from aiodataloader import DataLoader
from aioextensions import collect
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from backend.typing import Project as Group
from users import domain as users_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> List[Group]:
    user_email: str = kwargs['user_email']

    active, inactive = await collect([
        users_domain.get_projects(user_email),
        users_domain.get_projects(user_email, active=False)
    ])
    user_groups = active + inactive

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(user_groups)

    return groups
