from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Decimal:
    return findings_domain.get_severity_score(parent.severity)
