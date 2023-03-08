from .schema import (
    BILLING,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    Price,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@BILLING.field("prices")
@require_login
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **_kwargs: None
) -> dict[str, Price]:
    return billing_domain.get_prices()
