from custom_exceptions import (
    OrganizationNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
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
