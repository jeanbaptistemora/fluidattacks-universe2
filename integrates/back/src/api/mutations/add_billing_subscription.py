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
    AddBillingSubscriptionPayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
    Dict,
    Optional,
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
) -> AddBillingSubscriptionPayload:
    group = await info.context.loaders.group.load(kwargs["group_name"])
    org = await info.context.loaders.organization.load(group["organization"])
    org_billing_customer: Optional[str] = org["billing_customer"]
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    # Create customer if it does not exist
    if org_billing_customer is None:
        customer: Customer = await billing_domain.create_customer(
            org_name=org["name"],
            user_email=user_email,
        )
        await orgs_domain.update_billing_customer(
            org_id=org["id"],
            org_name=org["name"],
            org_billing_customer=customer.id,
        )
        org_billing_customer = customer.id

    # Create checkout session
    checkout: AddBillingSubscriptionPayload = (
        await billing_domain.create_checkout(
            subscription=kwargs["subscription"],
            org_billing_customer=org_billing_customer,
            org_name=org["name"],
            group_name=group["name"],
            previous_checkout_id=group["billing_checkout_id"],
        )
    )

    # Update group with new billing checkout id
    await groups_domain.update_billing_checkout_id(
        group["name"],
        checkout.id,
    )

    return checkout
