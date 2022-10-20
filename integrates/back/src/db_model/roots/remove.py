# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
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


async def remove_environment_url(
    root_id: str,
    url_id: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_url"],
        values={"uuid": root_id, "hash": url_id},
    )
    await operations.delete_item(key=primary_key, table=TABLE)


async def remove_environment_url_secret(url_id: str, secret_key: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_environment_secret"],
        values={"hash": url_id, "key": secret_key},
    )
    await operations.delete_item(key=primary_key, table=TABLE)


async def remove_root_environment_url_secrets(
    *,
    url_id: str,
) -> None:
    facet = TABLE.facets["root_environment_secret"]
    primary_key = keys.build_key(
        facet=facet,
        values={"hash": url_id},
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(facet,),
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


async def remove_root_environment_urls(
    *,
    root_id: str,
) -> None:
    facet = TABLE.facets["root_environment_url"]
    primary_key = keys.build_key(
        facet=facet,
        values={"uuid": root_id},
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(facet,),
        table=TABLE,
    )
    if not response.items:
        return
    await collect(
        remove_root_environment_url_secrets(
            url_id=item["sk"].split("URL#")[-1]
        )
        for item in response.items
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


async def remove_root_machine_executions(
    *,
    root_id: str,
) -> None:
    facet = TABLE.facets["machine_git_root_execution"]
    primary_key = keys.build_key(
        facet=facet,
        values={"uuid": root_id},
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(facet,),
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


async def remove_secret(root_id: str, secret_key: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_secret"],
        values={"uuid": root_id, "key": secret_key},
    )
    await operations.delete_item(key=primary_key, table=TABLE)
