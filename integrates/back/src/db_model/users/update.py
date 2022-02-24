from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Any,
    Dict,
)


async def update_user(
    *, user_email: str, notifications_preferences: Dict[str, Any]
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["user_metadata"],
        values={"email": user_email},
    )

    await operations.update_item(
        item={"notifications_preferences": notifications_preferences},
        key=primary_key,
        table=TABLE,
    )
