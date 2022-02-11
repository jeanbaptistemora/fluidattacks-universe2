from billing import (
    domain as billing_domain,
)
from billing.types import (
    Price,
)
from custom_types import (
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
    Dict,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    _parent: Organization, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, Price]:
    return await billing_domain.get_prices()
