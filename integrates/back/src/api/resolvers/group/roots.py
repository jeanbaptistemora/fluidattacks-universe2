from .schema import (
    GROUP,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@GROUP.field("roots")
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Root]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name

    return await loaders.group_roots.load(group_name)
