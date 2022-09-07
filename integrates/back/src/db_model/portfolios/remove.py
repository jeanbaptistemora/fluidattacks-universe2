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


async def remove(*, organization_name: str, portfolio_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["portfolio_metadata"],
        values={
            "id": portfolio_id,
            "name": organization_name,
        },
    )
    await operations.delete_item(key=primary_key, table=TABLE)
