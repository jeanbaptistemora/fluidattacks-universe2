from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)


async def remove(*, filename: str, group_name: str, root_id: str) -> None:
    toe_lines_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "group_name": group_name,
            "root_id": root_id,
            "filename": filename,
        },
    )
    await operations.delete_item(primary_key=toe_lines_key, table=TABLE)
