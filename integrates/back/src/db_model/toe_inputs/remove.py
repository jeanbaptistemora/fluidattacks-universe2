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
    Item,
    PrimaryKey,
)


async def remove(
    *,
    entry_point: str,
    component: str,
    group_name: str,
    root_id: str,
) -> None:
    facet = TABLE.facets["toe_input_metadata"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": component,
            "entry_point": entry_point,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    await operations.delete_item(key=toe_input_key, table=TABLE)


async def remove_group_toe_inputs(
    *,
    group_name: str,
) -> None:
    facet = TABLE.facets["toe_input_metadata"]
    primary_key = keys.build_key(
        facet=facet,
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.sort_key.replace("#ROOT#COMPONENT#ENTRYPOINT", "")
            )
        ),
        facets=(TABLE.facets["toe_input_metadata"],),
        table=TABLE,
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


async def remove_items(*, items: tuple[Item, ...]) -> None:
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item["pk"],
                sort_key=item["sk"],
            )
            for item in items
        ),
        table=TABLE,
    )
