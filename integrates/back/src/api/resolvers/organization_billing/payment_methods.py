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
