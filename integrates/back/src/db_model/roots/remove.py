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
    Facet,
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


async def remove_secret(root_id: str, secret_key: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_secret"],
        values={"uuid": root_id, "key": secret_key},
    )
    await operations.delete_item(key=primary_key, table=TABLE)


async def _remove_environment_url_secrets(
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


async def _remove_all_environment_urls(
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
        _remove_environment_url_secrets(url_id=item["sk"].split("URL#")[-1])
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


async def _remove_root_facets(
    *, root_id: str, facets: tuple[Facet, ...]
) -> None:
    primary_key = keys.build_key(
        facet=facets[0],
        values={
            "uuid": root_id,
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=facets,
        table=TABLE,
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


async def remove(*, root_id: str) -> None:
    await _remove_all_environment_urls(root_id=root_id)
    await _remove_root_facets(
        root_id=root_id,
        facets=(
            TABLE.facets["git_root_historic_state"],
            TABLE.facets["ip_root_historic_state"],
            TABLE.facets["url_root_historic_state"],
        ),
    )
    await _remove_root_facets(
        root_id=root_id,
        facets=(TABLE.facets["git_root_historic_cloning"],),
    )
    await _remove_root_facets(
        root_id=root_id,
        facets=(TABLE.facets["root_secret"],),
    )
    await _remove_root_facets(
        root_id=root_id,
        facets=(TABLE.facets["machine_git_root_execution"],),
    )
    await _remove_root_facets(
        root_id=root_id,
        facets=(
            TABLE.facets["git_root_metadata"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["url_root_metadata"],
        ),
    )
