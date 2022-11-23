from boto3.dynamodb.conditions import (
    Key,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
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


async def remove(
    *,
    organization_id: str,
    organization_name: str,
) -> None:
    # Currently, a prefix could precede the organization id, let's remove it
    organization_id = remove_org_id_prefix(organization_id)

    primary_key = keys.build_key(
        facet=TABLE.facets["organization_metadata"],
        values={
            "id": organization_id,
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    )
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(
            TABLE.facets["organization_historic_policies"],
            TABLE.facets["organization_historic_state"],
            TABLE.facets["organization_metadata"],
        ),
        table=TABLE,
    )
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={
            "id": organization_id,
            "name": organization_name,
        },
    )
    keys_to_delete = tuple(
        PrimaryKey(
            partition_key=item[TABLE.primary_key.partition_key],
            sort_key=item[TABLE.primary_key.sort_key],
        )
        for item in response.items
    ) + (unreliable_indicators_key,)
    await operations.batch_delete_item(
        keys=tuple(set(keys_to_delete)),
        table=TABLE,
    )
