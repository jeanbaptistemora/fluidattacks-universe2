from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
    RootRequest,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: ToeLines,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Root:
    loaders: Dataloaders = info.context.loaders
    root: Root = await loaders.root.load(
        RootRequest(parent.group_name, parent.root_id)
    )

    return root
