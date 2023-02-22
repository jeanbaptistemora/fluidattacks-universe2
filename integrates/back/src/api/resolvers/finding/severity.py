from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("severity")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Finding20Severity | Finding31Severity:
    return parent.severity
