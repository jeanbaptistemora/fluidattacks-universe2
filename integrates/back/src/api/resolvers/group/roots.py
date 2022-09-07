# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Root, ...]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    roots: tuple[Root, ...] = await loaders.group_roots.load(group_name)

    return roots
