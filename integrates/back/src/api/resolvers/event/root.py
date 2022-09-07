# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.events.types import (
    Event,
)
from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(parent: Event, info: GraphQLResolveInfo) -> Optional[Root]:
    loaders: Dataloaders = info.context.loaders
    if parent.root_id:
        root: Root = await loaders.root.load(
            (parent.group_name, parent.root_id)
        )
        return root
    return None
