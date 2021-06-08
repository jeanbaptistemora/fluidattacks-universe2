# None


from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Project as Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Group:
    # Compatibility with the old API
    group_name: str
    if "group_name" in kwargs:
        group_name = kwargs["group_name"].lower()
    else:
        group_name = kwargs["project_name"].lower()
    group_loader: DataLoader = info.context.loaders.group
    group: Group = await group_loader.load(group_name.lower())

    return group
