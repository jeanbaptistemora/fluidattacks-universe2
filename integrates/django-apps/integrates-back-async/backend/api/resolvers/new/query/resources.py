# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import Project as Group, Resource, Resources


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Resources:
    group_name: str = kwargs['project_name'].lower()

    group_loader: DataLoader = info.context.loaders['group']
    group: Group = await group_loader.load(group_name)

    return {
        'environments': cast(List[Resource], group.get('environments', [])),
        'files': cast(List[Resource], group.get('files', [])),
        'project_name': group_name,
        'repositories': cast(List[Resource], group.get('repositories', []))
    }
