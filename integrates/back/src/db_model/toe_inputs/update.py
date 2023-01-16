from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeInput,
    ToeInputMetadataToUpdate,
    ToeInputState,
)
from .utils import (
    format_toe_input_item,
    format_toe_input_metadata_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidParameter,
    ToeInputAlreadyUpdated,
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


async def update_state(
    *,
    current_value: ToeInput,
    new_state: ToeInputState,
    metadata: ToeInputMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_input_metadata"]
    if new_state.modified_date is None:
        raise InvalidParameter("modified_date")
    if new_state.modified_by is None:
        raise InvalidParameter("modified_by")
    metadata_key = keys.build_key(
        facet=facet,
        values={
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.state.unreliable_root_id,
        },
    )
    current_gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(current_value.state.be_present).lower(),
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.state.unreliable_root_id,
        },
    )
    current_value_item = format_toe_input_item(
        metadata_key,
        key_structure,
        current_gsi_2_key,
        gsi_2_index,
        current_value,
    )
    metadata_item: Item = format_toe_input_metadata_item(new_state, metadata)

    if "be_present" in metadata_item:
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "be_present": str(metadata_item["be_present"]).lower(),
                "component": current_value.component,
                "entry_point": current_value.entry_point,
                "group_name": current_value.group_name,
                "root_id": current_value.state.unreliable_root_id,
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
            "root_id": current_value.state.unreliable_root_id,
            "iso8601utc": get_as_utc_iso_format(new_state.modified_date),
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
