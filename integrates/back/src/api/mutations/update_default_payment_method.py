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
    org = await info.context.loaders.organization.load(
        kwargs["organization_id"]
    )

    # Update default payment method
    result: bool = await billing_domain.update_default_payment_method(
        org_billing_customer=org["billing_customer"],
        payment_method_id=kwargs["payment_method_id"],
    )

    return SimplePayload(success=result)
