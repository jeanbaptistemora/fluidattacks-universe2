from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Project as Group,
    Resource,
    Resources,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Resources:
    group_name: str
    if "group_name" in kwargs:
        group_name = kwargs["group_name"].lower()
    else:
        group_name = kwargs["project_name"].lower()
    group_loader: DataLoader = info.context.loaders.group
    group: Group = await group_loader.load(group_name)

    return {
        "files": cast(List[Resource], group.get("files", [])),
        "project_name": group_name,
    }
