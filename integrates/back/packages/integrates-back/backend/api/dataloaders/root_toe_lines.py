# Standard libraries
from typing import (
    Tuple
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from data_containers.toe_lines import GitRootToeLines
from toe.lines import domain as toe_lines_domain


async def get_root_toe_lines(
    *,
    group_name: str,
    root_id: str
) -> Tuple[GitRootToeLines, ...]:
    root_toe_lines: Tuple[GitRootToeLines, ...] = (
        await toe_lines_domain.get_by_root(
            group_name=group_name,
            root_id=root_id
        )
    )

    return root_toe_lines


class RootToeLinesLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        roots: Tuple[Tuple[str, str], ...]
    ) -> Tuple[Tuple[GitRootToeLines, ...], ...]:
        return tuple(await collect(
            get_root_toe_lines(group_name=group_name, root_id=root_id)
            for group_name, root_id in roots
        ))
