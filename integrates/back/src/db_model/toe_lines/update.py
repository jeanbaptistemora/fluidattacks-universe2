from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeLines,
    ToeLinesMetadataToUpdate,
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
from db_model import (
    utils as db_model_utils,
)
from db_model.toe_lines.utils import (
    format_toe_lines_item,
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
from typing import (
    Dict,
    Union,
)


async def update_metadata(
    *,
    current_value: ToeLines,
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
    current_gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(current_value.be_present).lower(),
            "filename": current_value.filename,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
        },
    )
    current_value_item = format_toe_lines_item(
        metadata_key,
        key_structure,
        current_gsi_2_key,
        gsi_2_index,
        current_value,
    )
    metadata_item: Dict[str, Union[str, datetime]] = {
        key: db_model_utils.get_as_utc_iso_format(value)
        if isinstance(value, datetime)
        else value
        for key, value in metadata._asdict().items()
        if value is not None and key not in {"clean_be_present_until"}
    }
    if metadata.clean_be_present_until:
        metadata_item["be_present_until"] = ""

    conditions = (
        Attr(attr_name).eq(current_value_item[attr_name])
        for attr_name in metadata_item
        if current_value_item[attr_name] is not None
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
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
