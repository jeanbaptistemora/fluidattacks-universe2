# Standard
from typing import cast, List

# Third party
from aiodataloader import DataLoader

# Local
from backend.domain.project import finding_domain
from backend.typing import Finding
from backend.utils import aio


class GroupDraftsLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> List[List[Finding]]:
        return cast(
            List[List[Finding]],
            await aio.materialize(
                finding_domain.get_drafts_by_group(group_name)
                for group_name in group_names
            )
        )
