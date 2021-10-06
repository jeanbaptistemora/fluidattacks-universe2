from .types import (
    ToeInput,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    RepeatedToeInput,
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


async def add(*, toe_input: ToeInput) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_input"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": toe_input.component,
            "entry_point": toe_input.entry_point,
            "group_name": toe_input.group_name,
        },
    )
    toe_input_item = {
        key_structure.partition_key: toe_input_key.partition_key,
        key_structure.sort_key: toe_input_key.sort_key,
        **dict(toe_input._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_input_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToeInput() from ex
