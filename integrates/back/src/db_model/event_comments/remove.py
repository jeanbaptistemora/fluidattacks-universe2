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


async def remove_event_comments(
    *,
    event_id: str,
) -> None:
    facet = TABLE.facets["event_comment"]
    primary_key = keys.build_key(
        facet=facet,
        values={"event_id": event_id},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.sort_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.partition_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(facet,),
        table=TABLE,
        index=index,
    )
    if not response.items:
        return
    keys_to_delete = set(
        PrimaryKey(
            partition_key=item[TABLE.primary_key.partition_key],
            sort_key=item[TABLE.primary_key.sort_key],
        )
        for item in response.items
    )
    await operations.batch_delete_item(
        keys=tuple(keys_to_delete),
        table=TABLE,
    )
