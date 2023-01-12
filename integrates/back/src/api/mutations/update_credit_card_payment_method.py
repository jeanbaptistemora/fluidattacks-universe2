from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from db_model.organizations.types import (
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
    org: Organization = await info.context.loaders.organization.load(
        kwargs["organization_id"]
    )

    result: bool = await billing_domain.update_credit_card_payment_method(
        org=org,
        payment_method_id=kwargs["payment_method_id"],
        card_expiration_month=kwargs["card_expiration_month"],
        card_expiration_year=kwargs["card_expiration_year"],
        make_default=kwargs["make_default"],
    )

    return SimplePayload(success=result)
