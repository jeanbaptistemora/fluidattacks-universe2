from .schema import (
    TAG,
)
from db_model.portfolios.types import (
    Portfolio,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TAG.field("lastClosedVulnerability")
def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int | None:
    return parent.unreliable_indicators.last_closing_date
