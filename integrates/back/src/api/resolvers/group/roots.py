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


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Root, ...]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    roots: tuple[RootItem, ...] = await loaders.group_roots.load(group_name)

    return tuple(roots_domain.format_root(root) for root in roots)
