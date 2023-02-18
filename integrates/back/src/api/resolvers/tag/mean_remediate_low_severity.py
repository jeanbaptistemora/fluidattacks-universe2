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
from typing import (
    Optional,
)


@TAG.field("meanRemediateLowSeverity")
async def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[Decimal]:
    mean_remediate_low_severity = (
        parent.unreliable_indicators.mean_remediate_low_severity
    )
    return mean_remediate_low_severity
