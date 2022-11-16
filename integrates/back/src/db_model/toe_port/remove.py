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


async def remove(
    *,
    group_name: str,
    ip: str,  # pylint: disable=invalid-name
    port: str,
    root_id: str,
) -> None:
    facet = TABLE.facets["toe_port_metadata"]
    toe_port_key = keys.build_key(
        facet=facet,
        values={
            "ip": ip,
            "port": port,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    await operations.delete_item(key=toe_port_key, table=TABLE)
