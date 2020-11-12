# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from aioextensions import collect

# Local
from backend.domain import root as root_domain
from backend.typing import Root


class GroupRootsLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(self, group_names: List[str]) -> List[List[Root]]:
        return cast(
            List[List[Root]],
            await collect(
                root_domain.get_roots_by_group(group_name)
                for group_name in group_names
            )
        )
