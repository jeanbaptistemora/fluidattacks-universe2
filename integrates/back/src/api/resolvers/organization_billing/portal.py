from billing import (
    domain as billing_domain,
)
from billing.types import (
    OrganizationBilling,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    utils as orgs_utils,
)
from sessions import (
    domain as sessions_domain,
)


async def resolve(
    parent: OrganizationBilling,
    info: GraphQLResolveInfo,
    **_kwargs: datetime,
) -> str:
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, parent.organization
    )
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    return await billing_domain.customer_portal(
        org_id=organization.id,
        org_name=organization.name,
        user_email=user_email,
        org_billing_customer=organization.billing_customer,
    )
