from aiodataloader import (
    DataLoader,
)
from custom_types import (
    Project as GroupType,
)
from typing import (
    List,
)


# pylint: disable=too-few-public-methods
class GroupActiveLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    def __init__(self, dataloader: DataLoader) -> None:
        super(GroupActiveLoader, self).__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(self, group_names: List[str]) -> List[GroupType]:
        groups: List[GroupType] = await self.dataloader.load_many(group_names)
        return groups
