# Standard libraries
from typing import (
    cast,
    List
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend.typing import Finding
from findings import domain as findings_domain


class GroupFindingsLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> List[List[Finding]]:
        return cast(
            List[List[Finding]],
            await collect([
                findings_domain.get_findings_by_group(
                    group_name,
                    include_deleted=True
                )
                for group_name in group_names
            ])
        )
