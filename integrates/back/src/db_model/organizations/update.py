from .types import (
    OrganizationMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    OrganizationNotFound,
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
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def update_metadata(
    *,
    metadata: OrganizationMetadataToUpdate,
    organization_id: str,
    organization_name: str,
) -> None:
    key_structure = TABLE.primary_key
    organization_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={
            "id": remove_org_id_prefix(organization_id),
            "name": organization_name,
        },
    )
    organization_item = format_metadata_item(metadata)
    if organization_item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=organization_item,
                key=organization_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise OrganizationNotFound() from ex
