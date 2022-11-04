# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from billing import (
    domain as billing_domain,
)
from billing.types import (
    OrganizationBilling,
)
from datetime import (
    datetime,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
    token as token_utils,
)


@concurrent_decorators(
    enforce_organization_level_auth_async,
    require_login,
)
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> OrganizationBilling:
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return await billing_domain.get_organization_billing(
        date=kwargs.get("date", datetime_utils.get_now()),
        org=parent,
        loaders=info.context.loaders,
        user_email=user_email,
    )
