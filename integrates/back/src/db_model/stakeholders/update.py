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
    email: str,
) -> None:
    email = email.strip().lower()
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    item = format_metadata_item(email, metadata)
    await operations.update_item(
        item=item,
        key=primary_key,
        table=TABLE,
    )
