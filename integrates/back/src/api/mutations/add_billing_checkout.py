from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
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
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> AddBillingCheckoutPayload:
    tier: str = kwargs["tier"]
    group_name: str = kwargs["group"]
    org_id: str = await orgs_domain.get_id_for_group(group_name)
    org_name: str = await orgs_domain.get_name_by_id(org_id)

    return await billing_domain.checkout(
        tier=tier,
        org_name=org_name,
        group_name=group_name,
    )
