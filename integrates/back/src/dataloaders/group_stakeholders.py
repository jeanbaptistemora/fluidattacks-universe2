from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders.stakeholder import (
    get_stakeholder,
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


async def _get_stakeholder(email: str) -> Stakeholder:
    try:
        stakeholder = await get_stakeholder(email=email)
    except StakeholderNotFound:
        stakeholder = Stakeholder(
            email=email,
            is_registered=False,
        )
    return stakeholder


async def get_group_stakeholders(
    group_name: str,
) -> tuple[Stakeholder, ...]:
    group_stakeholders_emails: list[str] = list(
        chain.from_iterable(
            await collect(
                [
                    get_group_users(group=group_name, active=True),
                    get_group_users(group=group_name, active=False),
                ]
            )
        )
    )
    group_stakeholders = await collect(
        tuple(_get_stakeholder(email) for email in group_stakeholders_emails)
    )

    return group_stakeholders


class GroupStakeholdersLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: Iterable[str]
    ) -> tuple[tuple[Stakeholder], ...]:
        return await collect(
            get_group_stakeholders(group_name) for group_name in group_names
        )
