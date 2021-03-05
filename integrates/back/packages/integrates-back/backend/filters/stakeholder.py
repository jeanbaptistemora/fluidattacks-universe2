from typing import List

from aioextensions import (
    collect,
)

from newutils import user as user_utils


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
