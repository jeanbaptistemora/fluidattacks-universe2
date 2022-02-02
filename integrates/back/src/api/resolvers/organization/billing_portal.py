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
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Dict,
    Optional,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Organization, info: GraphQLResolveInfo, **_kwargs: None
) -> Portal:
    org_id: str = parent["id"]
    org_name: str = parent["name"]
    org_billing_customer: Optional[str] = parent.get("billing_customer", None)
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return await billing_domain.create_portal(
        org_id=org_id,
        org_name=org_name,
        user_email=user_email,
        org_billing_customer=org_billing_customer,
    )
