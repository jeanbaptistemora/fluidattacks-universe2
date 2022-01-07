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
    enforce_group_level_auth_async,
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
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    group = await info.context.loaders.group.load(kwargs["group_name"])
    org = await info.context.loaders.organization.load(group["organization"])

    result: bool = await billing_domain.remove_subscription(
        org_billing_customer=org["billing_customer"],
        group_name=group["name"],
    )
    return SimplePayload(success=result)
