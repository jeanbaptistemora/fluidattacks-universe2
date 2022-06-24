from .types import (
    StakeholderMetadataToUpdate,
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
    metadata: StakeholderMetadataToUpdate,
    stakeholder_email: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": stakeholder_email},
    )
    item = format_metadata_item(metadata)
    if item:
        await operations.update_item(
            item=item,
            key=primary_key,
            table=TABLE,
        )
