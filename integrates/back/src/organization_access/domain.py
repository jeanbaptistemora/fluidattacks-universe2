import authz
from dataloaders import (
    Dataloaders,
)
from db_model.organization_access.types import (
    OrganizationAccessRequest,
)


async def has_access(
    loaders: Dataloaders, organization_id: str, email: str
) -> bool:
    if (
        await authz.get_organization_level_role(
            loaders, email, organization_id
        )
        == "admin"
    ):
        return True

    if await loaders.organization_access.load(
        OrganizationAccessRequest(organization_id=organization_id, email=email)
    ):
        return True
    return False
