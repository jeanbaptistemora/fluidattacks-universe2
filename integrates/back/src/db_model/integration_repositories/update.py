from .types import (
    OrganizationIntegrationRepository,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb import (
    keys,
    operations,
)


async def update_unreliable_repositories(
    *,
    repository: OrganizationIntegrationRepository,
) -> None:
    organization_id = remove_org_id_prefix(repository.organization_id)
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        values={
            "id": organization_id,
            "hash": repository.id,
            "branch": repository.branch.lower(),
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        "branch": repository.branch,
        "last_commit_date": get_as_utc_iso_format(repository.last_commit_date)
        if repository.last_commit_date
        else None,
        "url": repository.url,
    }

    await operations.put_item(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        item=item,
        table=TABLE,
    )
