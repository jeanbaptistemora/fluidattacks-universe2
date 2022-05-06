from billing import (
    domain as billing_domain,
)
from db_model.organization.types import (
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
    Any,
    Optional,
    Union,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Union[Organization, dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    if isinstance(parent, dict):
        org_id: str = parent["id"]
        org_name: str = parent["name"]
        org_billing_customer: Optional[str] = parent.get(
            "billing_customer", None
        )
    else:
        org_id = parent.id
        org_name = parent.name
        org_billing_customer = parent.billing_customer
    user_info: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return await billing_domain.customer_portal(
        org_id=org_id,
        org_name=org_name,
        user_email=user_email,
        org_billing_customer=org_billing_customer,
    )
