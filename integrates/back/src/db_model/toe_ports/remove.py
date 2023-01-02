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


async def remove(
    *,
    group_name: str,
    address: str,
    port: str,
    root_id: str,
) -> None:
    facet = TABLE.facets["toe_port_metadata"]
    toe_port_key = keys.build_key(
        facet=facet,
        values={
            "address": address,
            "port": port,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    await remove_historic_toe_ports(
        address=address,
        port=port,
        group_name=group_name,
        root_id=root_id,
    )
    await operations.delete_item(key=toe_port_key, table=TABLE)


async def remove_group_toe_ports(
    *,
    group_name: str,
) -> None:
    facet = TABLE.facets["toe_port_metadata"]
    primary_key = keys.build_key(
        facet=facet,
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.sort_key.replace("#ROOT#ADDRESS#PORT", "")
            )
        ),
        facets=(TABLE.facets["toe_port_metadata"],),
        table=TABLE,
    )
    await collect(
        tuple(
            remove_historic_toe_ports(
                address=item["address"],
                port=item["port"],
                group_name=item["group_name"],
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


async def remove_historic_toe_ports(
    address: str, port: str, group_name: str, root_id: str
) -> None:
    historic_toe_port_key = keys.build_key(
        facet=TABLE.facets["toe_port_historic_state"],
        values={
            "address": address,
            "port": port,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(
                historic_toe_port_key.partition_key
            )
            & Key(key_structure.sort_key).begins_with("STATE#")
        ),
        facets=(TABLE.facets["toe_port_historic_state"],),
        table=TABLE,
    )
    if response.items:
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
