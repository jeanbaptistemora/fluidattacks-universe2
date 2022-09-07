# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    _parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    return set()
