from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeLines,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    RepeatedToeLines,
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


async def add(*, toe_lines: ToeLines) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["toe_lines_metadata"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": toe_lines.filename,
            "group_name": toe_lines.group_name,
            "root_id": toe_lines.root_id,
        },
    )
    toe_lines_item = format_toe_lines_item(
        toe_lines_key, key_structure, toe_lines
    )
    condition_expression = Attr(key_structure.partition_key).not_exists()
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(toe_lines.be_present).lower(),
            "filename": toe_lines.filename,
            "group_name": toe_lines.group_name,
            "root_id": toe_lines.root_id,
        },
    )
    gsi_2_index = TABLE.indexes["gsi_2"]
    toe_lines_item[gsi_2_index.primary_key.sort_key] = gsi_2_key.sort_key
    toe_lines_item[
        gsi_2_index.primary_key.partition_key
    ] = gsi_2_key.partition_key
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_lines_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToeLines() from ex
