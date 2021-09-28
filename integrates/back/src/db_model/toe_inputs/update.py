from .types import (
    ToeInput,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)


async def update(*, root_toe_input: ToeInput) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_input"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": root_toe_input.component,
            "entry_point": root_toe_input.entry_point,
            "group_name": root_toe_input.group_name,
        },
    )
    toe_input = {
        key_structure.partition_key: toe_input_key.partition_key,
        key_structure.sort_key: toe_input_key.sort_key,
        **root_toe_input._asdict(),
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=toe_input,
        table=TABLE,
    )
