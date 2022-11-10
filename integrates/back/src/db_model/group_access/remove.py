# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    batch_delete_item,
    delete_item,
    query,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, email: str, group_name: str) -> None:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": email,
            "name": group_name,
        },
    )

    await delete_item(key=primary_key, table=TABLE)

    historic_key = keys.build_key(
        facet=TABLE.facets["group_historic_access"],
        values={
            "email": email,
            "name": group_name,
        },
    )
    key_structure = TABLE.primary_key
    response = await query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
        ),
        facets=(TABLE.facets["group_historic_access"],),
        table=TABLE,
    )
    await batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )
