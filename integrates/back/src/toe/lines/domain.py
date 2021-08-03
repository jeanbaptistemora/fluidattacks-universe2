from data_containers.toe_lines import (
    GitRootToeLines,
)
from toe.lines import (
    dal as toe_lines_dal,
)
from typing import (
    Tuple,
)


async def add(root_toe_lines: GitRootToeLines) -> None:
    await toe_lines_dal.add(root_toe_lines)


async def remove(filename: str, group_name: str, root_id: str) -> None:
    await toe_lines_dal.remove(filename, group_name, root_id)


async def get_by_group(group_name: str) -> Tuple[GitRootToeLines, ...]:
    return await toe_lines_dal.get_by_group(group_name)


async def get_by_root(
    group_name: str, root_id: str
) -> Tuple[GitRootToeLines, ...]:
    return await toe_lines_dal.get_by_root(group_name, root_id)


async def update(root_toe_lines: GitRootToeLines) -> None:
    await toe_lines_dal.update(root_toe_lines)
