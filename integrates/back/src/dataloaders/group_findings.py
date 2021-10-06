from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from typing import (
    cast,
    List,
)


class GroupFindingsLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> List[List[Finding]]:
        return cast(
            List[List[Finding]],
            await collect(
                [
                    findings_domain.get_findings_by_group(
                        group_name, include_deleted=True
                    )
                    for group_name in group_names
                ]
            ),
        )
