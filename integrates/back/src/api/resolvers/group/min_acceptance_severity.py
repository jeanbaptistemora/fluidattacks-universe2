# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.groups.types import (
    Group,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.groups import (
    get_group_min_acceptance_severity,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal:

    return await get_group_min_acceptance_severity(
        loaders=info.context.loaders,
        group=parent,
    )
