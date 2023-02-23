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


@TAG.field("meanRemediate")
async def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal | None:
    mean_remediate = parent.unreliable_indicators.mean_remediate
    return mean_remediate
