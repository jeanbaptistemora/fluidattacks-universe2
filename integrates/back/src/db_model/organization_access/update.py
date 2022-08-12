from .types import (
    OrganizationAccessMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
    operations,
)


async def update_metadata(
    *,
    email: str,
    metadata: OrganizationAccessMetadataToUpdate,
    organization_id: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": email,
            "id": remove_org_id_prefix(organization_id),
        },
    )
    item = format_metadata_item(
        email=email, metadata=metadata, organization_id=organization_id
    )
    await operations.update_item(
        item=item,
        key=primary_key,
        table=TABLE,
    )
