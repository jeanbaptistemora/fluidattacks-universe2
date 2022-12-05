from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToePort,
    ToePortMetadataToUpdate,
)
from .utils import (
    format_state_item,
    format_toe_port_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidParameter,
    ToePortAlreadyUpdated,
)
from datetime import (
    datetime,
)
from db_model import (
    utils as db_model_utils,
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
from dynamodb.types import (
    Item,
)


def _format_metadata_item(metadata: ToePortMetadataToUpdate) -> Item:
    metadata_item: Item = {
        key: db_model_utils.get_as_utc_iso_format(value)
        if isinstance(value, datetime)
        else value
        for key, value in metadata._asdict().items()
        if value is not None
        and key
        not in {
            "clean_attacked_at",
            "clean_be_present_until",
            "clean_first_attack_at",
            "clean_seen_at",
            "state",
        }
    }
    metadata_item["state"] = format_state_item(metadata.state)
    if metadata.clean_attacked_at:
        metadata_item["attacked_at"] = None
    if metadata.clean_be_present_until:
        metadata_item["be_present_until"] = None
    if metadata.clean_first_attack_at:
        metadata_item["first_attack_at"] = None
    if metadata.clean_seen_at:
        metadata_item["seen_at"] = None

    return metadata_item


async def update_metadata(
    *, current_value: ToePort, metadata: ToePortMetadataToUpdate
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_port_metadata"]
    metadata_key = keys.build_key(
        facet=facet,
        values={
            "group_name": current_value.group_name,
            "address": current_value.address,
            "port": current_value.port,
            "root_id": current_value.root_id,
        },
    )
    current_gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(current_value.be_present).lower(),
            "group_name": current_value.group_name,
            "address": current_value.address,
            "port": current_value.port,
            "root_id": current_value.root_id,
        },
    )
    current_value_item = format_toe_port_item(
        metadata_key,
        key_structure,
        current_gsi_2_key,
        gsi_2_index,
        current_value,
    )
    metadata_item = _format_metadata_item(metadata)
    conditions = tuple(
        Attr(attr_name).not_exists()
        if current_value_item[attr_name] is None
        else Attr(attr_name).eq(current_value_item[attr_name])
        for attr_name in metadata_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    if "be_present" in metadata_item:
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "be_present": str(metadata_item["be_present"]).lower(),
                "group_name": current_value.group_name,
                "address": current_value.address,
                "port": current_value.port,
                "root_id": current_value.root_id,
            },
        )
        gsi_2_index = TABLE.indexes["gsi_2"]
        metadata_item[gsi_2_index.primary_key.sort_key] = gsi_2_key.sort_key
    try:
        if metadata_item:
            await operations.update_item(
                condition_expression=condition_expression,
                item=metadata_item,
                key=metadata_key,
                table=TABLE,
            )
    except ConditionalCheckFailedException as ex:
        raise ToePortAlreadyUpdated() from ex

    if not isinstance(metadata_item["state"]["modified_date"], str):
        raise InvalidParameter("modified_date")

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_port_historic_metadata"],
        values={
            "address": current_value.address,
            "port": current_value.port,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
            "iso8601utc": metadata_item["state"]["modified_date"],
        },
    )
    await operations.put_item(
        facet=TABLE.facets["toe_port_historic_metadata"],
        item={
            **dict(current_value_item | metadata_item),
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
