from boto3.dynamodb.conditions import (
    Key,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, group_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={
            "name": group_name,
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    )
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(
            TABLE.facets["group_historic_policies"],
            TABLE.facets["group_historic_state"],
            TABLE.facets["group_metadata"],
            TABLE.facets["group_unreliable_indicators"],
        ),
        table=TABLE,
    )
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
