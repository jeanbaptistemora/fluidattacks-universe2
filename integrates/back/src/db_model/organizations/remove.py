# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def remove_unreliable_indicators(
    *,
    organization_id: str,
    organization_name: str,
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_unreliable_indicators"],
        values={
            "id": organization_id,
            "name": organization_name,
        },
    )
    await operations.delete_item(key=primary_key, table=TABLE)
