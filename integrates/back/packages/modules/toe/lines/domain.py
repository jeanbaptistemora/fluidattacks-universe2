# Standard libraries
from typing import Tuple

# Local libraries
from toe.lines import dal as toe_lines_dal
from dynamodb.types import GitRootToeLines


async def get_by_root(
    group_name: str,
    root_id: str
) -> Tuple[GitRootToeLines, ...]:
    return await toe_lines_dal.get_by_root(
        group_name=group_name,
        root_id=root_id
    )


async def update(root_toe_lines: GitRootToeLines) -> None:
    await toe_lines_dal.update(root_toe_lines)
