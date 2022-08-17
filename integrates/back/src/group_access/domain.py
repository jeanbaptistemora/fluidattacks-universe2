from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    InvalidAuthorization,
    RequestedInvitationTooSoon,
    StakeholderNotFound,
    StakeholderNotInGroup,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    group_access as group_access_model,
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
from itertools import (
    chain,
)
from jose import (
    JWTError,
)
from newutils import (
    datetime as datetime_utils,
    token as token_utils,
)
from newutils.datetime import (
    get_from_epoch,
    get_minus_delta,
    get_now,
)
from newutils.group_access import (
    format_invitation_state,
)
from typing import (
    Any,
)


async def add_access(
    loaders: Any, email: str, group_name: str, role: str
) -> None:
    await group_access_model.update_metadata(
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            has_access=True,
        ),
    )
    await authz.grant_group_level_role(loaders, email, group_name, role)


async def get_access_by_url_token(loaders: Any, url_token: str) -> GroupAccess:
    try:
        token_content = token_utils.decode_jwt(url_token)
        group_name: str = token_content["group_name"]
        email: str = token_content["user_email"]
    except (JWTError, KeyError) as ex:
        raise InvalidAuthorization() from ex

    return await loaders.group_access.load((group_name, email))


async def get_reattackers(
    loaders: Any, group_name: str, active: bool = True
) -> list[str]:
    stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active
    )
    stakeholder_roles = await collect(
        authz.get_group_level_role(loaders, email, group_name)
        for email in stakeholders
    )
    return [
        str(stakeholder)
        for stakeholder, stakeholder_role in zip(
            stakeholders, stakeholder_roles
        )
        if stakeholder_role == "reattacker"
    ]


async def _get_stakeholder(loaders: Any, email: str) -> Stakeholder:
    try:
        return await loaders.stakeholder.load(email)
    except StakeholderNotFound:
        return Stakeholder(
            email=email,
            is_registered=False,
        )


async def get_group_stakeholders(
    loaders: Any,
    group_name: str,
) -> tuple[Stakeholder, ...]:
    stakeholders_emails: list[str] = list(
        chain.from_iterable(
            await collect(
                [
                    get_group_stakeholders_emails(
                        loaders, group_name=group_name, active=True
                    ),
                    get_group_stakeholders_emails(
                        loaders, group_name=group_name, active=False
                    ),
                ]
            )
        )
    )
    return await collect(
        tuple(
            _get_stakeholder(loaders, email) for email in stakeholders_emails
        )
    )


async def get_group_stakeholders_emails(
    loaders: Any, group_name: str, active: bool = True
) -> list[str]:
    stakeholders_access: tuple[
        GroupAccess
    ] = await loaders.group_stakeholders_access.load(group_name)
    now_epoch = datetime_utils.get_as_epoch(datetime_utils.get_now())
    not_expired_stakeholders_access = tuple(
        access
        for access in stakeholders_access
        if not access.expiration_time or access.expiration_time > now_epoch
    )
    return [
        access.email
        for access in not_expired_stakeholders_access
        if access.has_access == active
    ]


async def get_managers(loaders: Any, group_name: str) -> list[str]:
    stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active=True
    )
    stakeholders_roles = await collect(
        [
            authz.get_group_level_role(loaders, stakeholder, group_name)
            for stakeholder in stakeholders
        ]
    )
    return [
        email
        for email, role in zip(stakeholders, stakeholders_roles)
        if role in {"user_manager", "vulnerability_manager"}
    ]


async def get_stakeholder_groups_names(
    loaders: Any, email: str, active: bool
) -> list[str]:
    groups_access: tuple[
        GroupAccess, ...
    ] = await loaders.stakeholder_groups_access.load(email)
    return [
        group_access.group_name
        for group_access in groups_access
        if group_access.has_access == active
    ]


async def get_stakeholders_to_notify(
    loaders: Any, group_name: str, active: bool = True
) -> list[str]:
    return await get_group_stakeholders_emails(loaders, group_name, active)


async def get_stakeholders_email_by_preferences(
    *,
    loaders: Any,
    group_name: str,
    notification: str,
    roles: set[str],
) -> list[str]:
    email_list = await get_stakeholders_email_by_roles(
        loaders=loaders,
        group_name=group_name,
        roles=roles,
    )
    stakeholders_data: tuple[
        Stakeholder, ...
    ] = await loaders.stakeholder.load_many(email_list)
    stakeholders_email = [
        stakeholder.email
        for stakeholder in stakeholders_data
        if notification in stakeholder.notifications_preferences.email
    ]
    return stakeholders_email


async def get_stakeholders_email_by_roles(
    *,
    loaders: Any,
    group_name: str,
    roles: set[str],
) -> list[str]:
    stakeholders = await get_group_stakeholders_emails(
        loaders, group_name, active=True
    )
    stakeholder_roles = await collect(
        tuple(
            authz.get_group_level_role(loaders, stakeholder, group_name)
            for stakeholder in stakeholders
        )
    )
    email_list = [
        str(stakeholder)
        for stakeholder, stakeholder_role in zip(
            stakeholders, stakeholder_roles
        )
        if stakeholder_role in roles
    ]
    return email_list


async def exists(loaders: Any, group_name: str, email: str) -> bool:
    try:
        await loaders.group_access.load((group_name, email))
        return True
    except StakeholderNotInGroup:
        return False


async def remove_access(loaders: Any, email: str, group_name: str) -> None:
    await group_access_model.remove(email=email, group_name=group_name)

    if email and group_name:
        me_vulnerabilities: tuple[
            Vulnerability, ...
        ] = await loaders.me_vulnerabilities.load(email)
        me_drafts: tuple[Finding, ...] = await loaders.me_drafts.load(email)
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


async def update(
    email: str,
    group_name: str,
    metadata: GroupAccessMetadataToUpdate,
) -> None:
    await group_access_model.update_metadata(
        email=email, group_name=group_name, metadata=metadata
    )


def validate_new_invitation_time_limit(inv_expiration_time: int) -> bool:
    """Validates that new invitations to the same user in the same group/org
    are spaced out by at least one minute to avoid email flooding."""
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
    if not await exists(loaders, group_name, email):
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
        else await authz.get_group_level_role(loaders, email, group_name)
    )
