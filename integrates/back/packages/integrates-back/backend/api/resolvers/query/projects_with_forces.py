# Standard
from typing import List

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import project as project_domain
from backend.typing import Project as Group


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _: None,
    info: GraphQLResolveInfo,
) -> List[Group]:
    projects = await project_domain.get_projects_with_forces()

    group_loader: DataLoader = info.context.loaders.group
    groups: List[Group] = await group_loader.load_many(projects)

    return groups
