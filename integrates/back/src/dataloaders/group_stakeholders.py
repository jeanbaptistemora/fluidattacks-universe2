from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
import authz
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
    get_invitation_state,
)
from typing import (
    cast,
    List,
    Tuple,
)


async def format_group_stakeholder(email: str, group_name: str) -> Stakeholder:
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
    invitation_state = get_invitation_state(invitation, stakeholder)
    if invitation_state == "PENDING":
        responsibility = invitation["responsibility"]
        group_role = invitation["role"]
    else:
        responsibility = cast(str, group_access.get("responsibility", ""))
        group_role = await authz.get_group_level_role(email, group_name)

    stakeholder = stakeholder._replace(
        responsibility=responsibility,
        invitation_state=invitation_state,
        role=group_role,
    )
    return stakeholder


async def get_group_stakeholders(
    group_name: str,
) -> list[Stakeholder]:
    group_stakeholders_emails = cast(
        list[str],
        list(
            chain.from_iterable(
                await collect(
                    [
                        get_group_users(group_name),
                        get_group_users(group_name, False),
                    ]
                )
            )
        ),
    )
    group_stakeholders = await collect(
        tuple(
            format_group_stakeholder(email, group_name)
            for email in group_stakeholders_emails
        )
    )

    return group_stakeholders


class GroupStakeholdersLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[List[Stakeholder], ...]:
        return await collect(
            (get_group_stakeholders(group_name) for group_name in group_names)
        )
