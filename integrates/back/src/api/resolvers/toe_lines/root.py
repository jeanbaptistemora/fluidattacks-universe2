from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(parent: ToeLines, info: GraphQLResolveInfo) -> RootItem:
    loaders: Dataloaders = info.context.loaders
    root: RootItem = await loaders.root.load(
        (parent.group_name, parent.root_id)
    )
    return root
