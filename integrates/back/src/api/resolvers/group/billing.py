# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from billing import (
    domain as billing_domain,
)
from billing.types import (
    GroupBilling,
)
from datetime import (
    datetime,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_service_white,
    require_login,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> GroupBilling:
    return await billing_domain.get_group_authors(
        date=kwargs.get("date", datetime_utils.get_now()),
        group=parent,
    )
