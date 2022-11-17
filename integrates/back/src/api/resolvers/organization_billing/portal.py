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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)


async def resolve(
    parent: OrganizationBilling,
    info: GraphQLResolveInfo,
    **_kwargs: datetime,
) -> str:
    org: Organization = await info.context.loaders.organization.load(
        parent.organization,
    )
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    return await billing_domain.customer_portal(
        org_id=org.id,
        org_name=org.name,
        user_email=user_email,
        org_billing_customer=org.billing_customer,
    )
