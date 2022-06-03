from billing import (
    domain as billing_domain,
)
from billing.types import (
    PaymentMethod,
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
from typing import (
    List,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[PaymentMethod]:
    org_billing_customer = parent.billing_customer
    return await billing_domain.customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=100,
    )
