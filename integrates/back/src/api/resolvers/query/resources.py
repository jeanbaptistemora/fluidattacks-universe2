from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Group,
    Resource,
    Resources,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
    get_present_key,
)
from typing import (
    cast,
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Resources:
    group_name: str
    group_name = get_key_or_fallback(kwargs).lower()
    group_name_key = get_present_key(kwargs)
    group_loader: DataLoader = info.context.loaders.group
    group: Group = await group_loader.load(group_name)

    return {
        "files": cast(List[Resource], group.get("files", [])),
        f"{group_name_key}": group_name,
    }
