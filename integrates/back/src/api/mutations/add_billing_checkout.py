from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    Customer,
)
from custom_types import (
    AddBillingCheckoutPayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> AddBillingCheckoutPayload:
    tier: str = kwargs["tier"]
    group_name: str = kwargs["group_name"]
    org_id: str = await orgs_domain.get_id_for_group(group_name)
    org_name: str = await orgs_domain.get_name_by_id(org_id)
    org_billing_customer: str = await orgs_domain.get_billing_customer_by_id(
        org_id,
    )
    user_email: str = (
        await token_utils.get_jwt_content(
            info.context,
        )
    )["user_email"]

    # Create customer if it does not exist
    if org_billing_customer == "":
        customer: Customer = await billing_domain.create_customer(
            org_name=org_name,
            user_email=user_email,
        )
        await orgs_domain.update_billing_customer(
            org_id=org_id,
            org_name=org_name,
            org_billing_customer=customer.id,
        )
        org_billing_customer = await orgs_domain.get_billing_customer_by_id(
            org_id,
        )

    return await billing_domain.checkout(
        tier=tier,
        org_billing_customer=org_billing_customer,
        org_name=org_name,
        group_name=group_name,
    )
