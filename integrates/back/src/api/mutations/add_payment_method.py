from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from custom_types import (
    SimplePayload,
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
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    org = await info.context.loaders.organization.load(
        kwargs["organization_id"]
    )
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    # Create payment method
    result: bool = await billing_domain.create_payment_method(
        org_billing_customer=org["billing_customer"],
        org_id=org["id"],
        org_name=org["name"],
        user_email=user_email,
        card_number=kwargs["card_number"],
        card_expiration_month=kwargs["card_expiration_month"],
        card_expiration_year=kwargs["card_expiration_year"],
        card_cvc=kwargs["card_cvc"],
        make_default=kwargs["make_default"],
    )

    return SimplePayload(success=result)
