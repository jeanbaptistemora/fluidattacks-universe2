from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToePort,
)
from .utils import (
    format_toe_port_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidParameter,
    RepeatedToePort,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.model import (
    TABLE,
)


async def add(*, toe_port: ToePort) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_port_metadata"]
    toe_port_key = keys.build_key(
        facet=facet,
        values={
            "address": toe_port.address,
            "port": toe_port.port,
            "group_name": toe_port.group_name,
            "root_id": toe_port.root_id,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(toe_port.be_present).lower(),
            "address": toe_port.address,
            "port": toe_port.port,
            "group_name": toe_port.group_name,
            "root_id": toe_port.root_id,
        },
    )
    toe_port_item = format_toe_port_item(
        toe_port_key, key_structure, gsi_2_key, gsi_2_index, toe_port
    )
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_port_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToePort() from ex

    if not isinstance(toe_port_item["state"]["modified_date"], str):
        raise InvalidParameter("modified_date")

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_port_historic_metadata"],
        values={
            "address": toe_port.address,
            "port": toe_port.port,
            "group_name": toe_port.group_name,
            "root_id": toe_port.root_id,
            "iso8601utc": toe_port_item["state"]["modified_date"],
        },
    )
    await operations.put_item(
        facet=TABLE.facets["toe_port_historic_metadata"],
        item={
            **toe_port_item,
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
