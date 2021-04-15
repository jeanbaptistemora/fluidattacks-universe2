# Standard libraries
from typing import (
    Tuple,
)

# Local libraries
from data_containers.toe_lines import GitRootToeLines
from toe.lines import dal as toe_lines_dal


async def add(root_toe_lines: GitRootToeLines) -> None:
    await toe_lines_dal.create(root_toe_lines)


async def delete(
    filename: str,
    group_name: str,
    root_id: str
) -> None:
    await toe_lines_dal.delete(
        filename,
        group_name,
        root_id
    )


async def get_by_group(
    group_name: str
) -> Tuple[GitRootToeLines, ...]:
    return await toe_lines_dal.get_by_group(group_name)


async def get_by_root(
    group_name: str,
    root_id: str
) -> Tuple[GitRootToeLines, ...]:
    return await toe_lines_dal.get_by_root(
        group_name,
        root_id
    )


async def update(root_toe_lines: GitRootToeLines) -> None:
    await toe_lines_dal.update(root_toe_lines)
