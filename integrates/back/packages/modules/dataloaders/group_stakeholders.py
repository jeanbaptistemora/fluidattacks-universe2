from typing import (
    List,
    Tuple,
    cast,
)

from aiodataloader import DataLoader
from aioextensions import collect

from custom_types import Stakeholder as StakeholderType
from users import domain as users_domain


class GroupStakeholdersLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[List[StakeholderType], ...]:
        return cast(
            Tuple[List[StakeholderType], ...],
            await collect(
                users_domain.get_stakeholders(group_name)
                for group_name in group_names
            ),
        )
