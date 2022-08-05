from .types import (
    StakeholderMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def update_metadata(
    *,
    metadata: StakeholderMetadataToUpdate,
    email: str,
) -> None:
    email = email.strip().lower()
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    item = format_metadata_item(email, metadata)
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=primary_key,
        table=TABLE,
    )
