from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    return "3.1" if isinstance(parent.severity, Finding31Severity) else "2.0"
