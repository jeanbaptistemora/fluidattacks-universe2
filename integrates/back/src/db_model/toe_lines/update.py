from .types import (
    ToeLines,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToeLinesNotFound,
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


async def update(*, toe_lines: ToeLines) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_lines"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": toe_lines.filename,
            "group_name": toe_lines.group_name,
            "root_id": toe_lines.root_id,
        },
    )
    toe_lines_item = {
        key_structure.partition_key: toe_lines_key.partition_key,
        key_structure.sort_key: toe_lines_key.sort_key,
        **dict(toe_lines._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_lines_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ToeLinesNotFound() from ex
