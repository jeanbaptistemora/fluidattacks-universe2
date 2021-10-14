from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    return parent.unreliable_indicators.unreliable_treatment_summary
