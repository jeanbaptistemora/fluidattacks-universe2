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
    metadata_item: Item = {
        key: get_as_utc_iso_format(value)
        if isinstance(value, datetime)
        else value
        for key, value in metadata._asdict().items()
        if value is not None and key not in {"clean_be_present_until", "state"}
    }
    metadata_item["state"] = {
        "modified_by": metadata.state.modified_by,
        "modified_date": get_as_utc_iso_format(metadata.state.modified_date)
        if metadata.state.modified_date
        else None,
    }
    if metadata.clean_be_present_until:
        metadata_item["be_present_until"] = None

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
