
from datetime import datetime
from graphql.type.definition import GraphQLResolveInfo

from model.findings.types import Finding
from newutils import datetime as datetime_utils


def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    report_date = ''
    if parent.unreliable_indicators.unreliable_report_date:
        date = datetime.fromisoformat(
            parent.unreliable_indicators.unreliable_report_date
        )
        report_date = datetime_utils.get_as_str(date)
    return report_date
