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


async def remove(*, filename: str, group_name: str, root_id: str) -> None:
    toe_lines_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "group_name": group_name,
            "root_id": root_id,
            "filename": filename,
        },
    )
    await operations.delete_item(key=toe_lines_key, table=TABLE)


async def remove_group_toe_lines(
    *,
    group_name: str,
) -> None:
    facet = TABLE.facets["toe_lines_metadata"]
    primary_key = keys.build_key(
        facet=facet,
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.sort_key.replace("#FILENAME", "")
            )
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
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
