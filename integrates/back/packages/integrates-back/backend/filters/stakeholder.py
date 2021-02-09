from typing import List, cast

from aioextensions import (
    collect,
)

from backend.typing import (
    Stakeholder as StakeholderType,
)
from backend.utils import (
    datetime as datetime_utils,
    user as user_utils,
)


def filter_by_expired_invitation(
    stakeholders: List[StakeholderType]
) -> List[StakeholderType]:
    return [
        stakeholder
        for stakeholder in stakeholders
        if not (
            stakeholder['invitation_state'] == 'PENDING'
            and stakeholder['invitation_date']
            and datetime_utils.get_plus_delta(
                datetime_utils.get_from_str(
                    cast(str, stakeholder['invitation_date'])
                ),
                weeks=1
            ) < datetime_utils.get_now()
        )
    ]


async def filter_non_fluid_staff(
    emails: List[str],
    group_name: str,
) -> List[str]:
    are_managers = await collect([
        user_utils.is_manager(email, group_name)
        for email in emails
    ])

    return [
        email
        for email, is_manager in zip(emails, are_managers)
        if not user_utils.is_fluid_staff(email) or is_manager
    ]
