# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(parent: ToeLines, info: GraphQLResolveInfo) -> Root:
    loaders: Dataloaders = info.context.loaders
    root: Root = await loaders.root.load((parent.group_name, parent.root_id))
    return root
