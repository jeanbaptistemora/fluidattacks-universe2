from db_model.portfolios.types import (
    Portfolio,
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
) -> Optional[int]:
    return parent.unreliable_indicators.last_closing_date
