from db_model import (
    TABLE,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)


async def remove(*, repository: OrganizationIntegrationRepository) -> None:
    organization_id = remove_org_id_prefix(repository.organization_id)
    credential_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_integration_repository"],
        values={
            "id": organization_id,
            "hash": repository.id.lstrip("URL#").split("#BRANCH#")[0],
            "branch": repository.branch.lower(),
        },
    )

    await operations.delete_item(key=credential_key, table=TABLE)
