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


async def remove(*, organization_name: str, portfolio_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["portfolio_metadata"],
        values={
            "id": portfolio_id,
            "name": organization_name,
        },
    )
    await operations.delete_item(key=primary_key, table=TABLE)


async def remove_organization_portfolios(
    *,
    organization_name: str,
) -> None:
    facet = TABLE.facets["portfolio_metadata"]
    primary_key = keys.build_key(
        facet=facet,
        values={"name": organization_name},
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
