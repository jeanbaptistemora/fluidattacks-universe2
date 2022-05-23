from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    RequestedInvitationTooSoon,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.findings.types import (
    Finding,
)
from db_model.users.types import (
    User,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.update import (
    update_assigned_index,
)
from group_access import (
    dal as group_access_dal,
)
from newutils.datetime import (
    get_from_epoch,
    get_minus_delta,
    get_now,
)
from typing import (
    Any,
    Dict,
    List,
    Set,
    Tuple,
)


async def add_user_access(email: str, group: str, role: str) -> bool:
    return await update_has_access(
        email, group, True
    ) and await authz.grant_group_level_role(email, group, role)


async def get_access_by_url_token(url_token: str) -> Dict[str, Any]:
    access: List[
        Dict[str, Any]
    ] = await group_access_dal.get_access_by_url_token(url_token)
    return access[0] if access else {}


async def get_reattackers(group_name: str, active: bool = True) -> List[str]:
    users = await get_group_users(group_name, active)
    user_roles = await collect(
        authz.get_group_level_role(user, group_name) for user in users
    )
    return [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role == "reattacker"
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
        if role in {"user_manager", "vulnerability_manager"}
    ]


async def get_user_access(user_email: str, group_name: str) -> Dict[str, Any]:
    access: List[Dict[str, Any]] = await group_access_dal.get_user_access(
        user_email, group_name
    )
    return access[0] if access else {}


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


async def get_users_email_by_preferences(
    *,
    loaders: Any,
    group_name: str,
    notification: str,
    roles: Set[str],
) -> List[str]:
    users = await get_group_users(group_name, active=True)
    user_roles = await collect(
        tuple(authz.get_group_level_role(user, group_name) for user in users)
    )
    email_list = [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role in roles
    ]
    users_data: tuple[User, ...] = await loaders.user.load_many(email_list)
    users_email = [
        user.email
        for user in users_data
        if notification in user.notifications_preferences.email
    ]
    return users_email


async def remove_access(
    loaders: Any, user_email: str, group_name: str
) -> bool:
    success: bool = all(
        await collect(
            [
                authz.revoke_group_level_role(user_email, group_name),
                group_access_dal.remove_access(user_email, group_name),
            ]
        )
    )
    if user_email and group_name:
        vulnerabilities: Tuple[
            Vulnerability, ...
        ] = await loaders.me_vulnerabilities.load(user_email)
        all_findings: Tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load(group_name)

        findings_ids: Set[str] = {finding.id for finding in all_findings}
        group_vulnerabilities: Tuple[Vulnerability, ...] = tuple(
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.finding_id in findings_ids
        )
        await collect(
            tuple(
                update_assigned_index(
                    finding_id=vulnerability.finding_id,
                    vulnerability_id=vulnerability.id,
                    entry=None,
                )
                for vulnerability in group_vulnerabilities
            )
        )
    return success


async def update(
    user_email: str, group_name: str, data: Dict[str, Any]
) -> bool:
    return await group_access_dal.update(user_email, group_name, data)


async def update_has_access(
    user_email: str, group_name: str, access: bool
) -> bool:
    return await update(user_email, group_name, {"has_access": access})


def validate_new_invitation_time_limit(inv_expiration_time: int) -> bool:
    """Validates that new invitations to the same user in the same group/org
    are spaced out by at least one minute to avoid email flooding"""
    expiration_date: datetime = get_from_epoch(inv_expiration_time)
    creation_date: datetime = get_minus_delta(date=expiration_date, weeks=1)
    current_date: datetime = get_now()
    if current_date - creation_date < timedelta(minutes=1):
        raise RequestedInvitationTooSoon()
    return True
