from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove_stakeholder(*, user_email: str) -> None:
    secret_key = keys.build_key(
        facet=TABLE.facets["user_metadata"],
        values={"email": user_email},
    )

    await delete_item(key=secret_key, table=TABLE)
