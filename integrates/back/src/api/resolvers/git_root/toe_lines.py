from dataloaders import (
    Dataloaders,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.types import (
    GitRoot,
)
from typing import (
    Tuple,
)


@enforce_group_level_auth_async
async def resolve(
    parent: GitRoot, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[ToeLines, ...]:
    loaders: Dataloaders = info.context.loaders
    root_toe_lines: Tuple[ToeLines, ...] = await loaders.root_toe_lines.load(
        (parent.group_name, parent.id)
    )

    return root_toe_lines
