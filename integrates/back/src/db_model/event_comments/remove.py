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
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, comment_id: str, event_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["event_comment"],
        values={
            "id": comment_id,
            "event_id": event_id,
        },
    )

    await operations.delete_item(key=primary_key, table=TABLE)


async def remove_event_comments(
    *,
    event_id: str,
) -> None:
    facet = TABLE.facets["event_comment"]
    primary_key = keys.build_key(
        facet=facet,
        values={"event_id": event_id},
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
