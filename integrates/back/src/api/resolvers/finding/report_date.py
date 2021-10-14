from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    report_date = ""
    unreliable_indicators = parent.unreliable_indicators
    if unreliable_indicators.unreliable_oldest_vulnerability_report_date:
        date = datetime.fromisoformat(
            unreliable_indicators.unreliable_oldest_vulnerability_report_date
        )
        report_date = datetime_utils.get_as_str(date)
    elif parent.creation:
        date = datetime.fromisoformat(parent.creation.modified_date)
        report_date = datetime_utils.get_as_str(date)
    return report_date
