# Standard
from typing import (
    cast,
    Tuple
)

# Third party
from aiodataloader import DataLoader
from aioextensions import collect

# Local
from backend.domain import root as root_domain
from backend.typing import Root


async def get_roots_by_group(group_name: str) -> Tuple[Root, ...]:
    return tuple(
        root_domain.format_root(root)
        for root in await root_domain.get_roots_by_group(group_name)
    )


class GroupRootsLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: Tuple[str, ...]
    ) -> Tuple[Tuple[Root, ...], ...]:
        return cast(Tuple[Tuple[Root, ...], ...], await collect(
            get_roots_by_group(group_name)
            for group_name in group_names
        ))
