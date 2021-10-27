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


async def update_metadata(
    *,
    current_value: ToeLines,
    group_name: str,
    filename: str,
    root_id: str,
    metadata: ToeLinesMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    current_value_item = format_toe_lines_item(
        metadata_key, key_structure, current_value
    )
    metadata_item = {
        key: value
        for key, value in metadata._asdict().items()
        if value is not None
    }
    conditions = (
        Attr(attr_name).eq(current_value_item[attr_name])
        for attr_name in metadata_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ToeLinesAlreadyUpdated() from ex
