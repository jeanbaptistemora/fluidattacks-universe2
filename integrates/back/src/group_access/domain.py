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
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from db_model.vulnerabilities.update import (
    update_assigned_index,
)
from dynamodb.types import (
    Item,
)
from group_access import (
    dal as group_access_dal,
)
from newutils import (
    stakeholders as stakeholders_utils,
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
    return users


async def get_users_email_by_preferences(
    *,
    loaders: Any,
    group_name: str,
    notification: str,
    roles: set[str],
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
    stakeholders_data: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(email_list)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders_data
        if notification in stakeholder.notifications_preferences.email
    ]
    return stakeholders_email


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


async def get_invitation_state(
    email: str,
    group_name: str,
    is_registered: bool,
) -> str:
    user_access = await get_user_access(email, group_name)
    invitation: Item = user_access.get("invitation", {})
    return stakeholders_utils.format_invitation_state(
        invitation, is_registered
    )


async def get_responsibility(
    email: str,
    group_name: str,
    is_registered: bool,
) -> str:
    user_access = await get_user_access(email, group_name)
    invitation: Item = user_access.get("invitation", {})
    invitation_state = stakeholders_utils.format_invitation_state(
        invitation, is_registered
    )
    return (
        invitation["responsibility"]
        if invitation_state == "PENDING"
        else user_access.get("responsibility", "")
    )


async def get_stakeholder_role(
    email: str,
    group_name: str,
    is_registered: bool,
) -> str:
    user_access = await get_user_access(email, group_name)
    invitation: Item = user_access.get("invitation", {})
    invitation_state = stakeholders_utils.format_invitation_state(
        invitation, is_registered
    )
    return (
        invitation["role"]
        if invitation_state == "PENDING"
        else await authz.get_group_level_role(email, group_name)
    )
