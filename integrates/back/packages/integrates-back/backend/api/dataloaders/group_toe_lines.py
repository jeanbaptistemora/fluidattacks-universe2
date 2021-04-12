# Standard libraries
from itertools import (
    groupby,
)
from typing import (
    List,
    Tuple
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend.api.dataloaders.root_toe_lines import RootToeLinesLoader
from data_containers.toe_lines import GitRootToeLines
from toe.lines import domain as toe_lines_domain


def get_root_key(toe_lines: GitRootToeLines) -> Tuple[str, str]:
    return (toe_lines.group_name, toe_lines.root_id)


async def get_group_toe_lines(
    *,
    group_name: str,
    root_toe_lines_loader: RootToeLinesLoader
) -> Tuple[GitRootToeLines, ...]:
    group_toe_lines: Tuple[GitRootToeLines, ...] = (
        await toe_lines_domain.get_by_group(group_name)
    )
    for key, root_toe_lines in groupby(group_toe_lines, get_root_key):
        root_toe_lines_loader.clear(key).prime(key, tuple(root_toe_lines))

    return group_toe_lines


class GroupToeLinesLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    def __init__(self, root_toe_lines_loader: RootToeLinesLoader) -> None:
        super(GroupToeLinesLoader, self).__init__()
        self.root_toe_lines_loader = root_toe_lines_loader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> Tuple[Tuple[GitRootToeLines, ...], ...]:
        return tuple(await collect(
            get_group_toe_lines(
                group_name=group_name,
                root_toe_lines_loader=self.root_toe_lines_loader
            )
            for group_name in group_names
        ))
