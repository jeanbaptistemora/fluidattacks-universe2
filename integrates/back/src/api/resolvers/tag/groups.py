# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.portfolios.types import (
    Portfolio,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    groups as groups_utils,
)


async def resolve(
    parent: Portfolio,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Group, ...]:
    group_names = parent.groups
    loaders: Dataloaders = info.context.loaders
    groups: tuple[Group, ...] = await loaders.group.load_many(group_names)
    return groups_utils.filter_active_groups(groups)
