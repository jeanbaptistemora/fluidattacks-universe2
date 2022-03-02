from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    RootItem,
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
    Dict,
    Tuple,
    Union,
)


async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Tuple[Root, ...]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)

    return tuple(roots_domain.format_root(root) for root in roots)
