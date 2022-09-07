# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, group_name: str, comment_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_comment"],
        values={
            "id": comment_id,
            "name": group_name,
        },
    )

    await delete_item(key=primary_key, table=TABLE)
