# Standard libraries

# Third-party libraries

# Local libraries
from backend.typing import ProjectAccess as GroupAccessType
from group_access import dal as group_access_dal


async def update(
    user_email: str,
    group_name: str,
    data: GroupAccessType
) -> bool:
    return await group_access_dal.update(user_email, group_name, data)
