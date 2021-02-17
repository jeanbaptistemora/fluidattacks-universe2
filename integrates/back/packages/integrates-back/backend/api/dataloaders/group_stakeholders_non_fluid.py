# Standard libraries
from typing import (
    cast,
    List,
    Tuple
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend.domain import (
    project as group_domain
)
from backend.filters import (
    stakeholder as stakeholder_filters
)
from backend.typing import (
    Stakeholder as StakeholderType
)


class GroupStakeholdersNonFluidLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""

    def __init__(self, dataloader: DataLoader) -> None:
        super(GroupStakeholdersNonFluidLoader, self).__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> Tuple[List[StakeholderType], ...]:
        groups_stakeholders = await self.dataloader.load_many(group_names)

        for index, group_stakeholders in enumerate(groups_stakeholders):
            group_name = group_names[index]
            group_stakeholders_emails = [
                stakeholder['email'] for stakeholder in group_stakeholders
            ]
            group_stakeholders_filtered_emails = (
                await stakeholder_filters.filter_non_fluid_staff(
                    group_stakeholders_emails,
                    group_name
                )
            )
            groups_stakeholders[index] = await collect(
                group_domain.format_stakeholder(email, group_name)
                for email in group_stakeholders_filtered_emails
            )

        return cast(Tuple[List[StakeholderType], ...], groups_stakeholders)
