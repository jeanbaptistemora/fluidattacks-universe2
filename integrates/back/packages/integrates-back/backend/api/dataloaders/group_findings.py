# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader
from aioextensions import collect

# Local
from backend.domain.project import finding_domain
from backend.typing import Finding


class GroupFindingsLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> List[List[Finding]]:
        return cast(
            List[List[Finding]],
            await collect(
                finding_domain.get_findings_by_group(group_name)
                for group_name in group_names
            )
        )
