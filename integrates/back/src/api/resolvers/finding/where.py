from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("where")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return parent.unreliable_indicators.unreliable_where
