from billing import (
    domain as billing_domain,
)
from billing.types import (
    Price,
)
from custom_types import (
    Group,
    Historic,
)
from datetime import (
    datetime,
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
    Dict,
    List,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_service_white,
    require_login,
)
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **kwargs: datetime
) -> Dict[str, Historic]:
    group_name: str = parent["name"]
    date: datetime = kwargs.get("date", datetime_utils.get_now())
    data: List[Dict[str, str]] = await billing_domain.get_authors_data(
        date=date,
        group=group_name,
    )
    total: int = len(data)
    current_spend: int = 0
    if parent["tier"] == "squad":
        prices: Dict[str, Price] = await billing_domain.get_prices()
        current_spend = total * prices["squad"].amount / 100
    else:
        current_spend = 0

    return {
        "current_spend": current_spend,
        "data": data,
        "total": total,
    }
