# Standard libraries
from typing import List

# Third party libraries
from aiodataloader import DataLoader

# Local libraries
from backend.exceptions import GroupNotFound
from backend.typing import Project as GroupType


def check_status(group: GroupType) -> GroupType:
    if group.get('project_status') == 'ACTIVE':
        return group

    raise GroupNotFound()


# pylint: disable=too-few-public-methods
class GroupActiveLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""

    def __init__(self, dataloader: DataLoader) -> None:
        super(GroupActiveLoader, self).__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(self, group_names: List[str]) -> List[GroupType]:
        groups: List[GroupType] = await self.dataloader.load_many(group_names)

        return [
            check_status(group)
            for group in groups
        ]
