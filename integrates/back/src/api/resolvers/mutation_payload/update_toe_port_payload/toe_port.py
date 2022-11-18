# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    UpdateToePortPayload,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.toe_ports.types import (
    ToePortRequest,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: UpdateToePortPayload, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[datetime]:
    loaders: Dataloaders = info.context.loaders
    request = ToePortRequest(
        address=parent.address,
        port=parent.port,
        group_name=parent.group_name,
        root_id=parent.root_id,
    )
    loaders.toe_port.clear(request)
    return await loaders.toe_port.load(request)
