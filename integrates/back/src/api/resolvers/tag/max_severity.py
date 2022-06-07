from db_model.portfolios.types import (
    Portfolio,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Decimal]:
    max_severity = parent.unreliable_indicators.max_severity
    return max_severity
