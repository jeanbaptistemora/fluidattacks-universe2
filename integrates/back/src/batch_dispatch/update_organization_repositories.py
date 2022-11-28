from azure_repositories.domain import (
    update_organization_repositories as update_repositories,
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


async def update_organization_repositories(*, item: BatchProcessing) -> None:
    organization_id: str = f'ORG#{item.entity.lstrip("org#")}'
    loaders: Dataloaders = get_new_context()
    organization: Organization = await loaders.organization.load(
        organization_id
    )
    all_group_names: set[str] = set(await get_all_active_group_names(loaders))

    await update_repositories(
        organization=organization,
        loaders=loaders,
        progress=0,
        all_group_names=all_group_names,
    )
