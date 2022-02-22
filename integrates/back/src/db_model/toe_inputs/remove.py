from db_model.toe_inputs.constants import (
    OLD_INPUT_FACET,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)


async def remove(
    *,
    entry_point: str,
    component: str,
    group_name: str,
    root_id: str,
) -> None:
    facet = TABLE.facets["toe_input_metadata"]
    toe_input_key = keys.build_key(
        facet=OLD_INPUT_FACET,
        values={
            "component": component,
            "entry_point": entry_point,
            "group_name": group_name,
        },
    )
    await operations.delete_item(key=toe_input_key, table=TABLE)
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": component,
            "entry_point": entry_point,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    await operations.delete_item(key=toe_input_key, table=TABLE)
