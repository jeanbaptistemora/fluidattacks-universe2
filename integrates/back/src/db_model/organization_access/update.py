from .types import (
    OrganizationAccessMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
    remove_org_id_prefix,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    StakeholderNotInOrganization,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def update_metadata(
    *,
    email: str,
    metadata: OrganizationAccessMetadataToUpdate,
    organization_id: str,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": email,
            "id": remove_org_id_prefix(organization_id),
        },
    )
    item = format_metadata_item(metadata)
    if item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=item,
                key=primary_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise StakeholderNotInOrganization() from ex
