# Standard libraries
from typing import (
    List,
    Tuple
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from data_containers.toe_lines import GitRootToeLines
from toe.lines import domain as toe_lines_domain


async def get_group_toe_lines(
    *,
    group_name: str
) -> Tuple[GitRootToeLines, ...]:
    group_toe_lines: Tuple[GitRootToeLines, ...] = (
        await toe_lines_domain.get_by_group(group_name)
    )

    return group_toe_lines


class GroupToeLinesLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> Tuple[Tuple[GitRootToeLines, ...], ...]:
        return tuple(await collect(
            get_group_toe_lines(
                group_name=group_name
            )
            for group_name in group_names
        ))
