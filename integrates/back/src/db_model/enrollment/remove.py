from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def remove(*, email: str) -> None:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["enrollment_metadata"],
        values={"email": email},
    )
    await operations.delete_item(key=primary_key, table=TABLE)
