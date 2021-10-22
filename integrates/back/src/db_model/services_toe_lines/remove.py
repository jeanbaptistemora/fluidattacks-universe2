from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)


async def remove(*, filename: str, group_name: str, root_id: str) -> None:
    facet = TABLE.facets["root_services_toe_lines"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    await operations.delete_item(primary_key=toe_lines_key, table=TABLE)
