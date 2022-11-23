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
    email = email.lower().strip()
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

    historic_key = keys.build_key(
        facet=TABLE.facets["group_historic_access"],
        values={
            "email": email,
            "name": group_name,
            # The modified date will always exist here
            "iso8601utc": metadata.state.modified_date
            if metadata.state.modified_date
            else "",
        },
    )
    key_structure = TABLE.primary_key
    await operations.put_item(
        facet=TABLE.facets["group_historic_access"],
        item={
            **item,
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
