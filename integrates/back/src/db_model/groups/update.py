from .types import (
    GroupMetadataToUpdate,
    GroupUnreliableIndicators,
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
from decimal import (
    Decimal,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


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


async def update_unreliable_indicators(
    *,
    group_name: str,
    indicators: GroupUnreliableIndicators,
) -> None:
    group_key = keys.build_key(
        facet=TABLE.facets["group_unreliable_indicators"],
        values={
            "name": group_name,
        },
    )
    unreliable_indicators = {
        key: Decimal(str(value)) if isinstance(value, float) else value
        for key, value in json.loads(json.dumps(indicators)).items()
    }
    await operations.update_item(
        item=unreliable_indicators,
        key=group_key,
        table=TABLE,
    )
