from .schema import (
    ORGANIZATION_BILLING,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    OrganizationBilling,
    PaymentMethod,
)
from dataloaders import (
    Dataloaders,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    utils as orgs_utils,
)


@ORGANIZATION_BILLING.field("paymentMethods")
async def resolve(
    parent: OrganizationBilling,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[PaymentMethod]:
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, parent.organization
    )

    return await billing_domain.customer_payment_methods(
        org=organization,
        limit=100,
    )
