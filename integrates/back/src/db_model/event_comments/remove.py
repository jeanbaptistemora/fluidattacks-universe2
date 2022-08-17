from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, comment_id: str, event_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_comment"],
        values={
            "id": comment_id,
            "event_id": event_id,
        },
    )

    await delete_item(key=primary_key, table=TABLE)
