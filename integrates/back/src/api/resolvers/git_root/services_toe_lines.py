from aiodataloader import (
    DataLoader,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
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
) -> Tuple[ServicesToeLines, ...]:
    group_name = parent.group_name
    root_id = parent.id
    root_toe_lines_loader: DataLoader = (
        info.context.loaders.root_services_toe_lines
    )
    root_services_toe_lines = await root_toe_lines_loader.load(
        (group_name, root_id)
    )

    return root_services_toe_lines
