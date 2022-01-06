from billing import (
    domain as billing_domain,
)
from billing.types import (
    Portal,
)
from custom_types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    parent: Organization, _info: GraphQLResolveInfo, **_kwargs: None
) -> Portal:
    org_name: str = parent["name"]
    org_billing_customer: str = parent.get("billing_customer", "")

    return await billing_domain.create_portal(
        org_name=org_name,
        org_billing_customer=org_billing_customer,
    )
