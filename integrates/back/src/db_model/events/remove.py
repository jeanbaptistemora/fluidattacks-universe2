# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


async def remove(*, event_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_metadata"],
        values={
            "id": event_id,
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    )
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(
            TABLE.facets["event_metadata"],
            TABLE.facets["event_historic_state"],
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
