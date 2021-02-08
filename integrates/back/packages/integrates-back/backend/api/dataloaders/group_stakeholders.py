# Standard libraries
from itertools import chain
from typing import (
    cast,
    List,
    Tuple
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend import authz
from backend.domain import (
    project as group_domain,
    user as stakeholder_domain
)
from backend.typing import (
    Invitation as InvitationType,
    Stakeholder as StakeholderType
)


async def _get_stakeholder(
    email: str,
    group_name: str
) -> StakeholderType:
    stakeholder: StakeholderType = await stakeholder_domain.get_by_email(email)
    project_access = await group_domain.get_user_access(
        email,
        group_name
    )
    invitation = cast(InvitationType, project_access.get('invitation'))
    invitation_state = (
        'PENDING' if invitation and not invitation['is_used'] else
        'UNREGISTERED' if not stakeholder.get('is_registered', False) else
        'CONFIRMED'
    )
    if invitation_state == 'PENDING':
        invitation_date = invitation['date']
        responsibility = invitation['responsibility']
        group_role = invitation['role']
        phone_number = invitation['phone_number']
    else:
        invitation_date = ''
        responsibility = cast(str, project_access.get('responsibility', ''))
        group_role = await authz.get_group_level_role(email, group_name)
        phone_number = cast(str, stakeholder['phone_number'])

    return {
        **stakeholder,
        'responsibility': responsibility,
        'invitation_date': invitation_date,
        'invitation_state': invitation_state,
        'phone_number': phone_number,
        'role': group_role
    }


async def get_stakeholders_by_group(
    group_name: str
) -> Tuple[StakeholderType, ...]:
    group_stakeholders_emails = cast(List[str], chain.from_iterable(
        await collect([
            group_domain.get_users(group_name),
            group_domain.get_users(group_name, False)
        ])
    ))
    group_stakeholders = cast(
        List[StakeholderType],
        await collect(
            _get_stakeholder(email, group_name)
            for email in group_stakeholders_emails
        )
    )

    return tuple(group_stakeholders)


class GroupStakeholdersLoader(DataLoader):  # type: ignore
    """Batches load calls within the same execution fragment."""
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        group_names: List[str]
    ) -> Tuple[Tuple[StakeholderType, ...], ...]:
        return cast(
            Tuple[Tuple[StakeholderType, ...], ...],
            await collect(
                get_stakeholders_by_group(group_name)
                for group_name in group_names
            )
        )
