from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeLines,
    ToeLinesMetadataToUpdate,
    ToeLinesState,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToeLinesAlreadyUpdated,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
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
import simplejson as json


async def update_state(
    *,
    current_value: ToeLines,
    new_state: ToeLinesState,
    metadata: ToeLinesMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    metadata_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "filename": current_value.filename,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
        },
    )
    base_item: Item = {
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
            "state",
        }
    }
    state_item: Item = json.loads(json.dumps(new_state, default=serialize))
    if metadata.clean_attacked_at:
        state_item["attacked_at"] = None
    if metadata.clean_be_present_until:
        state_item["be_present_until"] = None
    if metadata.clean_first_attack_at:
        state_item["first_attack_at"] = None
    metadata_item = base_item | {
        key: value
        for key, value in state_item.items()
        if key not in {"modified_by", "modified_date"}
    }
    metadata_item["state"] = {
        "modified_by": new_state.modified_by,
        "modified_date": get_as_utc_iso_format(new_state.modified_date)
        if new_state.modified_date
        else None,
    }

    condition_expression = Attr(key_structure.partition_key).exists()
    if current_value.state.modified_date is None:
        condition_expression &= Attr("state.modified_date").not_exists()
    else:
        condition_expression &= Attr("state.modified_date").eq(
            get_as_utc_iso_format(current_value.state.modified_date)
        )

    if "be_present" in metadata_item:
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "be_present": str(metadata_item["be_present"]).lower(),
                "filename": current_value.filename,
                "group_name": current_value.group_name,
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
        raise ToeLinesAlreadyUpdated() from ex
