from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, email: str) -> None:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )

    await delete_item(key=primary_key, table=TABLE)
