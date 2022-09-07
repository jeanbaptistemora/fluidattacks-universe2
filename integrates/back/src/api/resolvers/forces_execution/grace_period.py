# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.forces.types import (
    ForcesExecution,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], ForcesExecution],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    if isinstance(parent, dict):
        if parent.get("grace_period"):
            return int(str(parent["grace_period"]))
        return 0
    return parent.grace_period if parent.grace_period else 0
