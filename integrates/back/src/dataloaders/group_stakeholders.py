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
    get_user_access,
)
from itertools import (
    chain,
)
from newutils.stakeholders import (
    format_invitation_state,
)
from typing import (
    Iterable,
)


async def _get_stakeholder(email: str, group_name: str) -> Stakeholder:
    try:
        group_access, stakeholder = await collect(
            (
                get_user_access(email, group_name),
                get_stakeholder(email=email),
            )
        )
    except StakeholderNotFound:
        group_access = await get_user_access(email, group_name)
        stakeholder = Stakeholder(
            email=email,
            first_name="",
            last_name="",
            is_registered=False,
        )
    invitation = group_access.get("invitation")
    invitation_state = format_invitation_state(
        invitation, stakeholder.is_registered
    )
    if invitation_state == "PENDING":
        responsibility: str = invitation["responsibility"]
    else:
        responsibility = group_access.get("responsibility", "")

    stakeholder = stakeholder._replace(
        responsibility=responsibility,
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
        tuple(
            _get_stakeholder(email, group_name)
            for email in group_stakeholders_emails
        )
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
