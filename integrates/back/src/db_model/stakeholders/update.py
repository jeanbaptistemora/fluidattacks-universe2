from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Any,
)


async def update_metadata(
    *, stakeholder_email: str, notifications_preferences: dict[str, Any]
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": stakeholder_email},
    )

    await operations.update_item(
        item={"notifications_preferences": notifications_preferences},
        key=primary_key,
        table=TABLE,
    )
