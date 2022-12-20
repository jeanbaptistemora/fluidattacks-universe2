from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)


async def get_organization_name(loaders: Dataloaders, group_name: str) -> str:
    group: Group = await loaders.group.load(group_name)
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    return organization.name
