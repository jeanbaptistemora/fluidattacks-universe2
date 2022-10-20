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


async def remove_group_forces_executions(
    *,
    group_name: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["forces_execution"],
        values={"name": group_name},
    )
    index = TABLE.indexes["inverted_index"]
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.sort_key).eq(
        primary_key.sort_key
    ) & Key(key_structure.partition_key).begins_with(primary_key.partition_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["forces_execution"],),
        table=TABLE,
        index=index,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item["pk"],
                sort_key=item["sk"],
            )
            for item in response.items
        ),
        table=TABLE,
    )
