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
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
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
) -> AddBillingCheckoutPayload:
    tier: str = kwargs["tier"]
    group_name: str = kwargs["group_name"]
    org_id: str = await orgs_domain.get_id_for_group(group_name)
    org_name: str = await orgs_domain.get_name_by_id(org_id)
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return await billing_domain.checkout(
        tier=tier,
        org_name=org_name,
        group_name=group_name,
        user_email=user_email,
    )
