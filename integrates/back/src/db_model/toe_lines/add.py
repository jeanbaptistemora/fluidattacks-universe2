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
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_lines_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToeLines() from ex
