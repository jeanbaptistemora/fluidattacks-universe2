from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
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
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
    Dict,
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
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    # Create checkout session
    return await billing_domain.create_checkout(
        subscription=kwargs["subscription"],
        org_billing_customer=org["billing_customer"],
        org_id=org["id"],
        org_name=org["name"],
        group_name=group["name"],
        previous_checkout_id=group["billing_checkout_id"],
        user_email=user_email,
    )
