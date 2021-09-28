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
) -> None:
    facet = TABLE.facets["root_toe_input"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": component,
            "entry_point": entry_point,
            "group_name": group_name,
        },
    )
    await operations.delete_item(primary_key=toe_input_key, table=TABLE)
