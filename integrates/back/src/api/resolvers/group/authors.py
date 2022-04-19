from billing import (
    domain as billing_domain,
)
from billing.types import (
    Price,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Any,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_service_white,
    require_login,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> dict[str, Any]:
    group_name: str = parent.name
    date: datetime = kwargs.get("date", datetime_utils.get_now())
    data: list[dict[str, str]] = await billing_domain.get_authors_data(
        date=date,
        group=group_name,
    )
    total: int = len(data)
    current_spend: int = 0
    group_tier: GroupTier = parent.state.tier
    if group_tier == GroupTier.SQUAD:
        prices: dict[str, Price] = await billing_domain.get_prices()
        current_spend = int(total * prices["squad"].amount / 100)
    else:
        current_spend = 0

    return {
        "current_spend": current_spend,
        "data": data,
        "total": total,
    }
