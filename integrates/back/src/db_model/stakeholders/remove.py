from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, stakeholder_email: str) -> None:
    secret_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": stakeholder_email},
    )

    await delete_item(key=secret_key, table=TABLE)
