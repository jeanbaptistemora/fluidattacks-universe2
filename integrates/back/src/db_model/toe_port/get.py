# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    ToePort,
    ToePortRequest,
)
from .utils import (
    format_toe_port,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    ToePortNotFound,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)
from typing import (
    List,
    Tuple,
)


async def _get_toe_port(request: ToePortRequest) -> ToePort:
    primary_key = keys.build_key(
        facet=TABLE.facets["toe_port_metadata"],
        values={
            "ip": request.ip,
            "port": request.port,
            "group_name": request.group_name,
            "root_id": request.root_id,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(TABLE.facets["toe_port_metadata"],),
        table=TABLE,
    )
    if not response.items:
        raise ToePortNotFound()
    return format_toe_port(response.items[0])


class ToePortLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: List[ToePortRequest]
    ) -> Tuple[ToePort, ...]:
        return await collect(tuple(map(_get_toe_port, requests)))
