# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from billing import (
    domain as billing_domain,
)
from billing.types import (
    Price,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Dict,
)


@require_login
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, Price]:
    return await billing_domain.get_prices()
