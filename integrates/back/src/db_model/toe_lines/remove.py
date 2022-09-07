# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    await operations.delete_item(key=toe_lines_key, table=TABLE)
