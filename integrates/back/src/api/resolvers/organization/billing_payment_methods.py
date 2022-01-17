from billing import (
    domain as billing_domain,
)
from billing.types import (
    PaymentMethod,
)
from custom_types import (
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
    Optional,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Organization, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[PaymentMethod]:
    org_billing_customer: Optional[str] = parent.get("billing_customer", None)

    return await billing_domain.customer_payment_methods(
        org_billing_customer=org_billing_customer,
        limit=100,
    )
