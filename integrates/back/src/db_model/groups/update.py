from .types import (
    GroupMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
    remove_org_id_prefix,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    GroupNotFound,
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
    group_name: str,
    metadata: GroupMetadataToUpdate,
    organization_id: str,
) -> None:
    key_structure = TABLE.primary_key
    group_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={
            "name": group_name,
            "organization_id": remove_org_id_prefix(organization_id),
        },
    )
    group_item = format_metadata_item(metadata)
    if group_item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=group_item,
                key=group_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise GroupNotFound() from ex
