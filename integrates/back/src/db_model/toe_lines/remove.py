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


async def remove(*, filename: str, group_name: str, root_id: str) -> None:
    toe_lines_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "group_name": group_name,
            "root_id": root_id,
            "filename": filename,
        },
    )
    await remove_historic_toe_lines(
        filename=filename,
        group_name=group_name,
        root_id=root_id,
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
    await collect(
        tuple(
            remove_historic_toe_lines(
                filename=item["filename"],
                group_name=group_name,
                root_id=item["root_id"],
            )
            for item in response.items
        ),
        workers=8,
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


async def remove_historic_toe_lines(
    filename: str, group_name: str, root_id: str
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_lines_historic_metadata"],
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with("STATE#")
        ),
        facets=(TABLE.facets["toe_lines_historic_metadata"],),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )
