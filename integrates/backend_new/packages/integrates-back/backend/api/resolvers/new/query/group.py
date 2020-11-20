# Standard
# None

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.typing import Project as Group


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Group:
    group_name: str = kwargs['project_name']

    group_loader: DataLoader = info.context.loaders['group']
    group: Group = await group_loader.load(group_name.lower())

    return group
