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


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[RootItem, ...]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    roots: tuple[RootItem, ...] = await loaders.group_roots.load(group_name)

    return roots
