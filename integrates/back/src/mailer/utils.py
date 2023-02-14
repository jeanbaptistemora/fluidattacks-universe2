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


async def get_organization_name(loaders: Dataloaders, group_name: str) -> str:
    group: Group = await loaders.group.load(group_name)
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    return organization.name


async def get_organization_country(
    loaders: Dataloaders, group_name: str
) -> Optional[str]:
    group: Group = await loaders.group.load(group_name)
    organization = await loaders.organization.load(group.organization_id)
    if not organization:
        raise OrganizationNotFound()
    return organization.country


async def get_group_emails_by_notification(
    *,
    loaders: Dataloaders,
    group_name: str,
    notification: str,
) -> list[str]:
    return await get_stakeholders_email_by_preferences(
        loaders=loaders,
        group_name=group_name,
        notification=MAIL_PREFERENCES[notification]["email_preferences"],
        roles=MAIL_PREFERENCES[notification]["roles"],
        exclude_trial=MAIL_PREFERENCES[notification]["exclude_trial"],
        only_fluid_staff=MAIL_PREFERENCES[notification]["only_fluid_staff"],
    )
