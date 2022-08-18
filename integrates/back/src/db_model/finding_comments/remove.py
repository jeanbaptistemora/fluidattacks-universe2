from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, comment_id: str, finding_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_comment"],
        values={
            "id": comment_id,
            "finding_id": finding_id,
        },
    )

    await delete_item(key=primary_key, table=TABLE)
