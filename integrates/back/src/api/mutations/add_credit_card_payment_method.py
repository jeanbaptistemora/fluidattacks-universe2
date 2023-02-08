from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from custom_exceptions import (
    OrganizationNotFound,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
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
    loaders: Dataloaders = info.context.loaders
    organization = await loaders.organization.load(kwargs["organization_id"])
    if organization is None:
        raise OrganizationNotFound()

    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    # Create credit card payment method
    result: bool = await billing_domain.create_credit_card_payment_method(
        org=organization,
        user_email=user_email,
        card_number=kwargs["card_number"],
        card_expiration_month=kwargs["card_expiration_month"],
        card_expiration_year=kwargs["card_expiration_year"],
        card_cvc=kwargs["card_cvc"],
        make_default=kwargs["make_default"],
    )

    return SimplePayload(success=result)
