# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    UpdateToeLinesPayload,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    ToeLinesRequest,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: UpdateToeLinesPayload, info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[datetime]:
    loaders: Dataloaders = info.context.loaders
    request = ToeLinesRequest(
        filename=parent.filename,
        group_name=parent.group_name,
        root_id=parent.root_id,
    )
    loaders.toe_lines.clear(request)
    return await loaders.toe_lines.load(request)
