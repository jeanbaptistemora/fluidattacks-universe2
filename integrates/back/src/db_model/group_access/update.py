from .types import (
    GroupAccessMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
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
    email: str,
    group_name: str,
    metadata: GroupAccessMetadataToUpdate,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": email,
            "name": group_name,
        },
    )
    item = format_metadata_item(
        email=email,
        group_name=group_name,
        metadata=metadata,
    )
    await operations.update_item(
        item=item,
        key=primary_key,
        table=TABLE,
    )
