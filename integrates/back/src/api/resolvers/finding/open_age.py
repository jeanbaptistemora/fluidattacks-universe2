from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    unreliable_indicators = parent.unreliable_indicators
    return findings_domain.get_report_days(
        unreliable_indicators.unreliable_oldest_open_vulnerability_report_date
    )
