# Standard libraries
from itertools import (
    chain,
    repeat,
)
from typing import (
    Any,
    Tuple,
)

# Local libraries
from data_containers.toe_lines import GitRootToeLines
from toe.lines import dal as toe_lines_dal


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
    loaders: Any,
    group_name: str
) -> Tuple[GitRootToeLines, ...]:
    group_roots_loader = loaders.group_roots
    group_roots = await group_roots_loader.load(group_name)
    group_roots_ids = [
        root.id
        for root in group_roots
    ]
    root_toe_lines_loader = loaders.root_toe_lines
    root_toe_lines = await root_toe_lines_loader.load_many(
        zip(repeat(group_name), group_roots_ids)
    )

    return tuple(chain.from_iterable(root_toe_lines))


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
