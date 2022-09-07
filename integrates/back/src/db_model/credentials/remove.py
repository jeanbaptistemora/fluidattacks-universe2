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


async def remove(*, credential_id: str, organization_id: str) -> None:
    credential_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={
            "organization_id": organization_id,
            "id": credential_id,
        },
    )
    await operations.delete_item(key=credential_key, table=TABLE)
