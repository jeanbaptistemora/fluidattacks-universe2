# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from dynamodb.operations import (
    delete_item,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, group_name: str, comment_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_comment"],
        values={
            "id": comment_id,
            "name": group_name,
        },
    )

    await delete_item(key=primary_key, table=TABLE)


async def remove_group_comments(
    *,
    group_name: str,
) -> None:
    facet = TABLE.facets["group_comment"]
    primary_key = keys.build_key(
        facet=facet,
        values={"name": group_name},
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
