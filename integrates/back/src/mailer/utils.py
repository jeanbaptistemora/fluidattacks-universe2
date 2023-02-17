from aioextensions import (
    collect,
)
import authz
from custom_exceptions import (
    OrganizationNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from group_access.domain import (
    get_stakeholders_email_by_preferences,
)
from mailer.preferences import (
    MAIL_PREFERENCES,
)
from typing import (
    Optional,
)


async def get_available_notifications(
    loaders: Dataloaders, email: str
) -> list[str]:
    stakeholder_roles = await get_stakeholder_roles(loaders, email)
    available_notifications_by_template = [
        template["email_preferences"]
        for template in MAIL_PREFERENCES.values()
        if any(
            item in template["roles"]["group"]
            for item in stakeholder_roles["group"]
        )
        or any(
            item in template["roles"]["org"]
            for item in stakeholder_roles["org"]
        )
    ]
    return sorted(set(available_notifications_by_template))


async def get_group_emails_by_notification(
    *,
    loaders: Dataloaders,
    group_name: str,
    notification: str,
) -> list[str]:
    preferences = MAIL_PREFERENCES.get(notification, {})
    group_roles = preferences.get("roles", {}).get("group", {})
    return await get_stakeholders_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=preferences.get("email_preferences", ""),
        roles=group_roles,
        exclude_trial=preferences.get("exclude_trial", False),
        only_fluid_staff=preferences.get("only_fluid_staff", False),
    )


async def get_group_rol(
    loaders: Dataloaders, email: str, group_name: str
) -> str:
    return await authz.get_group_level_role(loaders, email, group_name)


async def get_org_groups(loaders: Dataloaders, org_id: str) -> list[Group]:
    return await loaders.organization_groups.load(org_id)


async def get_org_rol(loaders: Dataloaders, email: str, org_id: str) -> str:
    return await authz.get_organization_level_role(loaders, email, org_id)


async def get_organization_country(
    loaders: Dataloaders, group_name: str
) -> Optional[str]:
    group: Group = await loaders.group.load(group_name)
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    return organization.country


async def get_organization_name(loaders: Dataloaders, group_name: str) -> str:
    group: Group = await loaders.group.load(group_name)
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    return organization.name


async def get_stakeholder_roles(
    loaders: Dataloaders, email: str
) -> dict[str, set[str]]:
    stakeholder_orgs = await loaders.stakeholder_organizations_access.load(
        email
    )
    org_roles = await collect(
        [
            get_org_rol(loaders, email, org.organization_id)
            for org in stakeholder_orgs
        ]
    )
    org_groups = await collect(
        [
            get_org_groups(loaders, org.organization_id)
            for org in stakeholder_orgs
        ]
    )
    group_roles = await collect(
        [
            get_group_rol(loaders, email, item.name)
            for group in org_groups
            for item in group
        ]
    )
    return dict(
        group=set(" ".join(group_roles).split()),
        org=set(" ".join(org_roles).split()),
    )
