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


async def remove(*, vulnerability_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"id": vulnerability_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
        ),
        facets=(
            TABLE.facets["vulnerability_metadata"],
            TABLE.facets["vulnerability_historic_state"],
            TABLE.facets["vulnerability_historic_treatment"],
            TABLE.facets["vulnerability_historic_verification"],
            TABLE.facets["vulnerability_historic_zero_risk"],
        ),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )
