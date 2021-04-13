# Standard libraries
from typing import List

# Third-party libraries

# Local libraries
from backend import authz
from backend.typing import ProjectAccess as GroupAccessType
from group_access import dal as group_access_dal


async def add_user_access(email: str, group: str, role: str) -> bool:
    return (
        await update_has_access(email, group, True) and
        await authz.grant_group_level_role(email, group, role)
    )


async def get_user_groups(user_email: str, active: bool) -> List[str]:
    return await group_access_dal.get_user_groups(user_email, active)


async def remove_access(user_email: str, group_name: str) -> bool:
    return await group_access_dal.remove_access(user_email, group_name)


async def update(
    user_email: str,
    group_name: str,
    data: GroupAccessType
) -> bool:
    return await group_access_dal.update(user_email, group_name, data)


async def update_has_access(
    user_email: str,
    group_name: str,
    access: bool
) -> bool:
    return await update(user_email, group_name, {'has_access': access})
