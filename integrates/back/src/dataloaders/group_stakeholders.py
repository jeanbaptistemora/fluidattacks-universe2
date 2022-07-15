from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from group_access.domain import (
    get_group_users,
)
from itertools import (
    chain,
)
from typing import (
    Iterable,
)


async def _get_stakeholder(
    stakeholder_loader: DataLoader, email: str
) -> Stakeholder:
    try:
        return await stakeholder_loader.load(email)
    except StakeholderNotFound:
        return Stakeholder(
            email=email,
            is_registered=False,
        )


async def get_group_stakeholders(
    group_name: str,
    stakeholder_loader: DataLoader,
) -> tuple[Stakeholder, ...]:
    stakeholders_emails: list[str] = list(
        chain.from_iterable(
            await collect(
                [
                    get_group_users(group=group_name, active=True),
                    get_group_users(group=group_name, active=False),
                ]
            )
        )
    )
    return await collect(
        tuple(
            _get_stakeholder(stakeholder_loader, email)
            for email in stakeholders_emails
        )
    )


class GroupStakeholdersLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[Stakeholder], ...]:
        return await collect(
            get_group_stakeholders(group_name, self.dataloader)
            for group_name in group_names
        )
