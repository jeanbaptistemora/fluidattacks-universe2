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


@TAG.field("meanRemediateHighSeverity")
async def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Decimal | None:
    mean_remediate_high_severity = (
        parent.unreliable_indicators.mean_remediate_high_severity
    )
    return mean_remediate_high_severity
