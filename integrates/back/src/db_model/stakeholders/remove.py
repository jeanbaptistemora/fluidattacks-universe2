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


async def remove(*, email: str) -> None:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    )
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(
            TABLE.facets["stakeholder_metadata"],
            TABLE.facets["stakeholder_historic_state"],
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
