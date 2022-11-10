# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from billing import (
    domain as billing_domain,
)
from billing.types import (
    OrganizationBilling,
    PaymentMethod,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: OrganizationBilling,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[PaymentMethod]:
    org: Organization = await info.context.loaders.organization.load(
        parent.organization,
    )
    return await billing_domain.customer_payment_methods(
        org=org,
        limit=100,
    )
