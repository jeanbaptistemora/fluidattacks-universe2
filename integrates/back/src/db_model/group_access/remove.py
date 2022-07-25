from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, email: str, group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": email,
            "name": group_name,
        },
    )

    await delete_item(key=primary_key, table=TABLE)
