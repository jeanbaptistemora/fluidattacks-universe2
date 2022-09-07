# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


@require_login
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **_kwargs: str
) -> Dict[str, Any]:
    return {}
