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
from typing import (
    List,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Organization,
    **_kwargs: None,
) -> List[PaymentMethod]:
    return await billing_domain.customer_payment_methods(
        org=parent,
        limit=100,
    )
