from .schema import (
    TAG,
)
from db_model.portfolios.types import (
    Portfolio,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@TAG.field("name")
def resolve(
    parent: Portfolio,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    portfolio_name = parent.id
    return portfolio_name
