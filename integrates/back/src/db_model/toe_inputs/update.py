from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeInput,
    ToeInputMetadataToUpdate,
)
from .utils import (
    format_toe_input_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToeInputAlreadyUpdated,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    get_as_utc_iso_format,
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


async def update_metadata(
    *, current_value: ToeInput, metadata: ToeInputMetadataToUpdate
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_input_metadata"]
    metadata_key = keys.build_key(
        facet=facet,
        values={
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.unreliable_root_id,
        },
    )
    current_gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(current_value.be_present).lower(),
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.unreliable_root_id,
        },
    )
    current_value_item = format_toe_input_item(
        metadata_key,
        key_structure,
        current_gsi_2_key,
        gsi_2_index,
        current_value,
    )
    metadata_item: Item = {
        key: get_as_utc_iso_format(value)
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
    metadata_item["state"] = {
        "modified_by": metadata.state.modified_by,
        "modified_date": get_as_utc_iso_format(metadata.state.modified_date)
        if metadata.state.modified_date
        else "",
    }
    if metadata.clean_attacked_at:
        metadata_item["attacked_at"] = ""
    if metadata.clean_be_present_until:
        metadata_item["be_present_until"] = ""
    if metadata.clean_first_attack_at:
        metadata_item["first_attack_at"] = ""
    if metadata.clean_seen_at:
        metadata_item["seen_at"] = ""

    if "be_present" in metadata_item:
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "be_present": str(metadata_item["be_present"]).lower(),
                "component": current_value.component,
                "entry_point": current_value.entry_point,
                "group_name": current_value.group_name,
                "root_id": current_value.unreliable_root_id,
            },
        )
        gsi_2_index = TABLE.indexes["gsi_2"]
        metadata_item[gsi_2_index.primary_key.sort_key] = gsi_2_key.sort_key
    condition_expression = Attr(key_structure.partition_key).exists()
    if current_value.state.modified_date is None:
        condition_expression &= Attr("state.modified_date").not_exists()
    else:
        condition_expression &= Attr("state.modified_date").eq(
            get_as_utc_iso_format(current_value.state.modified_date)
        )
    try:
        if metadata_item:
            await operations.update_item(
                condition_expression=condition_expression,
                item=metadata_item,
                key=metadata_key,
                table=TABLE,
            )
    except ConditionalCheckFailedException as ex:
        raise ToeInputAlreadyUpdated() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_input_historic_metadata"],
        values={
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.unreliable_root_id,
            # The modified date will always exist here
            "iso8601utc": get_as_utc_iso_format(metadata.state.modified_date)
            if metadata.state.modified_date
            else "",
        },
    )
    await operations.put_item(
        facet=TABLE.facets["toe_input_historic_metadata"],
        item={
            **dict(current_value_item | metadata_item),
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
