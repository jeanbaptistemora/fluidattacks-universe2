from aioextensions import (
    collect,
)
import authz
from custom_types import (
    Group as GroupType,
    GroupAccess as GroupAccessType,
)
from group_access import (
    dal as group_access_dal,
)
from typing import (
    cast,
    Dict,
    List,
)


async def add_user_access(email: str, group: str, role: str) -> bool:
    return await update_has_access(
        email, group, True
    ) and await authz.grant_group_level_role(email, group, role)


async def get_access_by_url_token(url_token: str) -> GroupAccessType:
    access: List[
        Dict[str, GroupType]
    ] = await group_access_dal.get_access_by_url_token(url_token)
    return cast(GroupAccessType, access[0]) if access else {}


async def get_reattackers(group_name: str, active: bool = True) -> List[str]:
    users = await get_group_users(group_name, active)
    user_roles = await collect(
        authz.get_group_level_role(user, group_name) for user in users
    )
    return [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role in {"reattacker", "closer"}
    ]


async def get_group_users(group: str, active: bool = True) -> List[str]:
    return await group_access_dal.get_group_users(group, active)


async def get_managers(group_name: str) -> List[str]:
    users = await get_group_users(group_name, active=True)
    users_roles = await collect(
        [authz.get_group_level_role(user, group_name) for user in users]
    )
    return [
        user_email
        for user_email, role in zip(users, users_roles)
        if role == "customeradmin"
    ]


async def get_user_access(user_email: str, group_name: str) -> GroupAccessType:
    access: List[
        Dict[str, GroupType]
    ] = await group_access_dal.get_user_access(user_email, group_name)
    return cast(GroupAccessType, access[0]) if access else {}


async def get_user_groups(user_email: str, active: bool) -> List[str]:
    return await group_access_dal.get_user_groups(user_email, active)


async def get_users_to_notify(
    group_name: str, active: bool = True
) -> List[str]:
    users = await get_group_users(group_name, active)
    user_roles = await collect(
        authz.get_group_level_role(user, group_name) for user in users
    )
    return [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role != "executive"
    ]


async def list_system_owners(group: str) -> List[str]:
    users_active, users_inactive = await collect(
        [get_group_users(group, True), get_group_users(group, False)]
    )
    all_users = users_active + users_inactive
    users_roles = await collect(
        [authz.get_group_level_role(user, group) for user in all_users]
    )
    managers = [
        user
        for user, role in zip(all_users, users_roles)
        if role in {"system_owner", "group_manager"}
    ]
    return managers


async def list_internal_owners(group_name: str) -> List[str]:
    all_managers = await list_system_owners(group_name)
    internal_managers = [
        user for user in all_managers if user.endswith("@fluidattacks.com")
    ]
    return internal_managers


async def remove_access(user_email: str, group_name: str) -> bool:
    success: bool = all(
        await collect(
            [
                authz.revoke_group_level_role(user_email, group_name),
                group_access_dal.remove_access(user_email, group_name),
            ]
        )
    )
    return success


async def update(
    user_email: str, group_name: str, data: GroupAccessType
) -> bool:
    return await group_access_dal.update(user_email, group_name, data)


async def update_has_access(
    user_email: str, group_name: str, access: bool
) -> bool:
    return await update(user_email, group_name, {"has_access": access})
