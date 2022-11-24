from aioextensions import (
    collect,
)
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
    Item,
    PrimaryKey,
)
from itertools import (
    chain,
)


async def _get_historic_state_items(*, policy_id: str) -> tuple[Item, ...]:
    facet = TABLE.facets["org_finding_policy_historic_state"]
    primary_key = keys.build_key(
        facet=facet,
        values={"uuid": policy_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(facet,),
        table=TABLE,
    )

    return response.items


async def remove_org_finding_policies(*, organization_name: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": organization_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["org_finding_policy_metadata"],),
        index=index,
        table=TABLE,
    )
    if not response.items:
        return

    policies_ids = set(
        item[TABLE.primary_key.partition_key].split("#")[1]
        for item in response.items
    )
    historic_state_items: tuple[Item, ...] = tuple(
        chain.from_iterable(
            await collect(
                _get_historic_state_items(policy_id=policy_id)
                for policy_id in policies_ids
            )
        )
    )
    keys_to_delete = set(
        PrimaryKey(
            partition_key=item[TABLE.primary_key.partition_key],
            sort_key=item[TABLE.primary_key.sort_key],
        )
        for item in response.items + historic_state_items
    )
    await operations.batch_delete_item(
        keys=tuple(keys_to_delete),
        table=TABLE,
    )
