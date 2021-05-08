# Standard libraries
from itertools import chain
from typing import (
    List,
    cast,
)

# Third party libraries
from aiodataloader import DataLoader

# Local libraries
from backend.typing import Finding as FindingType
from newutils import findings as findings_utils


class GroupFindingsNonDeletedLoader(DataLoader):

    def __init__(self, dataloader: DataLoader) -> None:
        super(GroupFindingsNonDeletedLoader, self).__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self,
        group_names: List[str]
    ) -> List[List[FindingType]]:
        unchained_data = await self.load_many(group_names)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> List[List[FindingType]]:
        groups_findings = await self.dataloader.load_many(group_names)

        for index, group_findings in enumerate(groups_findings):
            groups_findings[index] = (
                findings_utils.filter_non_deleted_findings(group_findings)
            )
        return cast(List[List[FindingType]], groups_findings)
