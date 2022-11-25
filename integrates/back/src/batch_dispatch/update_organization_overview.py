from azure_repositories.domain import (
    update_organization_repositories,
    update_organization_unreliable,
)
from batch.types import (
    BatchProcessing,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.organizations.types import (
    Organization,
)
from organizations.domain import (
    get_all_active_group_names,
)


async def update_organization_overview(*, item: BatchProcessing) -> None:
    organization_id: str = item.entity
    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(
        organization_id
    )
    all_group_names: set[str] = set(await get_all_active_group_names(loaders))

    await update_organization_repositories(
        organization=organization,
        loaders=loaders,
        progress=0,
        all_group_names=all_group_names,
    )
    await update_organization_unreliable(
        organization=organization,
        loaders=loaders,
        progress=0,
        all_group_names=all_group_names,
    )
