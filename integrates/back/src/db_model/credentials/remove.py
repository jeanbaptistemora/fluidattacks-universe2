from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, credential_id: str, group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={"name": group_name, "uuid": credential_id},
    )
    index = TABLE.indexes["inverted_index"]
    response = await operations.query(
        condition_expression=(
            Key(index.primary_key.partition_key).eq(primary_key.sort_key)
            & Key(index.primary_key.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["credentials_metadata"],
            TABLE.facets["credentials_state"],
        ),
        index=index,
        table=TABLE,
    )

    await operations.batch_write_item(
        items=tuple(
            {
                **item,
                TABLE.primary_key.partition_key: (
                    f"REMOVED#{item[TABLE.primary_key.partition_key]}"
                ),
            }
            for item in response.items
        ),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[TABLE.primary_key.partition_key],
                sort_key=item[TABLE.primary_key.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )
