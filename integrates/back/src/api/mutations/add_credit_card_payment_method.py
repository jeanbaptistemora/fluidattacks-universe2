from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
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
from organizations import (
    utils as orgs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("addCreditCardPaymentMethod")
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
    organization = await orgs_utils.get_organization(
        loaders, kwargs["organization_id"]
    )
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    return SimplePayload(
        success=await billing_domain.create_credit_card_payment_method(
            org=organization,
            user_email=user_email,
            card_number=kwargs["card_number"],
            card_expiration_month=kwargs["card_expiration_month"],
            card_expiration_year=kwargs["card_expiration_year"],
            card_cvc=kwargs["card_cvc"],
            make_default=kwargs["make_default"],
        )
    )
