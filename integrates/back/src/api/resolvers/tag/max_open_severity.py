from .schema import (
    TAG,
)
from db_model.portfolios.types import (
    Portfolio,
)
from decimal import (
    Decimal,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TAG.field("maxOpenSeverity")
async def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal | None:
    max_open_severity = parent.unreliable_indicators.max_open_severity
    return max_open_severity
