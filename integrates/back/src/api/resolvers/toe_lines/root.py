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
from roots import (
    domain as roots_domain,
)
from roots.types import (
    Root,
)


async def resolve(
    parent: ToeLines, info: GraphQLResolveInfo, **_kwargs: None
) -> Root:
    loaders: Dataloaders = info.context.loaders
    root: RootItem = await loaders.root.load(
        (parent.group_name, parent.root_id)
    )
    return roots_domain.format_root(root)
