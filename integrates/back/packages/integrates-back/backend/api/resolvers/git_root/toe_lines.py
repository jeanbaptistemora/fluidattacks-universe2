# Standard
from typing import Tuple

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from data_containers.toe_lines import GitRootToeLines
from roots.types import GitRoot


async def resolve(
    parent: GitRoot,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> Tuple[GitRootToeLines, ...]:
    group_name = parent.group_name
    root_id = parent.id
    root_toe_lines_loader: DataLoader = info.context.loaders.root_toe_lines
    root_toe_lines = await root_toe_lines_loader.load((group_name, root_id))

    return root_toe_lines
