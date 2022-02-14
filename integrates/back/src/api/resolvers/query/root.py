from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    RootItem,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots import (
    domain as roots_domain,
)
from roots.types import (
    Root,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> Root:
    group_name: str = kwargs["group_name"]
    root_id: str = kwargs["root_id"]
    loaders: Dataloaders = info.context.loaders
    root: RootItem = await loaders.root.load((group_name, root_id))

    return roots_domain.format_root(root)
