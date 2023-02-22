from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_as_str,
)


@FINDING.field("reportDate")
def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str | None:
    unreliable_indicators = parent.unreliable_indicators
    if unreliable_indicators.unreliable_oldest_vulnerability_report_date:
        return get_as_str(
            unreliable_indicators.unreliable_oldest_vulnerability_report_date
        )
    if parent.creation:
        return get_as_str(parent.creation.modified_date)

    return None
