from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    InvalidAuthorization,
    RequestedInvitationTooSoon,
    StakeholderNotInGroup,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.findings.update import (
    update_me_draft_index,
)
from db_model.findings.utils import (
    filter_non_state_status_findings,
)
from db_model.group_access.enums import (
    GroupInvitiationState,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from jose import (
    JWTError,
)
from newutils.datetime import (
    get_from_epoch,
    get_minus_delta,
    get_now,
)
from newutils.group_access import (
    format_invitation_state,
)
from newutils.token import (
    decode_jwt,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    Any,
)


async def add_user_access(email: str, group_name: str, role: str) -> bool:
    await group_access_dal.add(
        group_access=GroupAccess(
            email=email, group_name=group_name, has_access=True
        )
    )
    return await authz.grant_group_level_role(email, group_name, role)


async def get_access_by_url_token(loaders: Any, url_token: str) -> GroupAccess:
    try:
        token_content = decode_jwt(url_token)
        group_name = str(get_key_or_fallback(token_content))
        user_email: str = token_content["user_email"]
    except JWTError:
        InvalidAuthorization()
    access: GroupAccess = await loaders.group_access.load(
        (group_name, user_email)
    )
    return access


async def get_reattackers(group_name: str, active: bool = True) -> list[str]:
    users = await get_group_users(group_name, active)
    user_roles = await collect(
        authz.get_group_level_role(user, group_name) for user in users
    )
    return [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role == "reattacker"
    ]


async def get_group_users(group: str, active: bool = True) -> list[str]:
    return await group_access_dal.get_group_users(group, active)


async def get_managers(group_name: str) -> list[str]:
    users = await get_group_users(group_name, active=True)
    users_roles = await collect(
        [authz.get_group_level_role(user, group_name) for user in users]
    )
    return [
        user_email
        for user_email, role in zip(users, users_roles)
        if role in {"user_manager", "vulnerability_manager"}
    ]


async def get_user_access(user_email: str, group_name: str) -> dict[str, Any]:
    access: list[dict[str, Any]] = await group_access_dal.get_user_access(
        user_email, group_name
    )
    return access[0] if access else {}


async def get_user_groups(user_email: str, active: bool) -> list[str]:
    return await group_access_dal.get_user_groups(user_email, active)


async def get_users_to_notify(
    group_name: str, active: bool = True
) -> list[str]:
    users = await get_group_users(group_name, active)
    return users


async def get_users_email_by_preferences(
    *,
    loaders: Any,
    group_name: str,
    notification: str,
    roles: set[str],
) -> list[str]:
    users = await get_group_users(group_name, active=True)
    user_roles = await collect(
        tuple(authz.get_group_level_role(user, group_name) for user in users)
    )
    email_list = [
        str(user)
        for user, user_role in zip(users, user_roles)
        if user_role in roles
    ]
    stakeholders_data: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(email_list)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders_data
        if notification in stakeholder.notifications_preferences.email
    ]
    return stakeholders_email


async def exist(loaders: Any, group_name: str, email: str) -> bool:
    try:
        await loaders.group_access.load((group_name, email))
        return True
    except StakeholderNotInGroup:
        return False


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
        me_vulnerabilities: tuple[
            Vulnerability, ...
        ] = await loaders.me_vulnerabilities.load(user_email)
        me_drafts: tuple[Finding, ...] = await loaders.me_drafts.load(
            user_email
        )
        all_findings: tuple[
            Finding, ...
        ] = await loaders.group_drafts_and_findings.load(group_name)

        drafts = filter_non_state_status_findings(
            all_findings,
            {
                FindingStateStatus.APPROVED,
                FindingStateStatus.DELETED,
            },
        )

        findings_ids: set[str] = {finding.id for finding in all_findings}
        drafts_ids: set[str] = {draft.id for draft in drafts}
        group_vulnerabilities: tuple[Vulnerability, ...] = tuple(
            vulnerability
            for vulnerability in me_vulnerabilities
            if vulnerability.finding_id in findings_ids
        )
        group_drafts: tuple[Finding, ...] = tuple(
            draft for draft in me_drafts if draft.id in drafts_ids
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
        await collect(
            tuple(
                update_me_draft_index(
                    finding_id=draft.id,
                    group_name=draft.group_name,
                    user_email="",
                )
                for draft in group_drafts
            )
        )
    return success


async def update(
    email: str,
    group_name: str,
    metadata: GroupAccessMetadataToUpdate,
) -> None:
    await group_access_dal.update_metadata(
        email=email, group_name=group_name, metadata=metadata
    )


def validate_new_invitation_time_limit(inv_expiration_time: int) -> bool:
    """Validates that new invitations to the same user in the same group/org
    are spaced out by at least one minute to avoid email flooding"""
    expiration_date: datetime = get_from_epoch(inv_expiration_time)
    creation_date: datetime = get_minus_delta(date=expiration_date, weeks=1)
    current_date: datetime = get_now()
    if current_date - creation_date < timedelta(minutes=1):
        raise RequestedInvitationTooSoon()
    return True


async def get_stakeholder_role(
    loaders: Any,
    email: str,
    group_name: str,
    is_registered: bool,
) -> str:
    if not await exist(loaders, group_name, email):
        group_access = GroupAccess(email=email, group_name=group_name)
    else:
        group_access = await loaders.group_access.load((group_name, email))
    group_invitation_state = format_invitation_state(
        invitation=group_access.invitation,
        is_registered=is_registered,
    )
    return (
        group_access.invitation.role
        if group_access.invitation
        and group_invitation_state == GroupInvitiationState.PENDING
        else await authz.get_group_level_role(email, group_name)
    )
