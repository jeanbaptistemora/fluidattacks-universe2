from db_model.findings.types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    convert_from_iso_str,
    get_as_str,
)
from typing import (
    Optional,
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[str]:
    unreliable_indicators = parent.unreliable_indicators
    if unreliable_indicators.unreliable_oldest_vulnerability_report_date:
        return convert_from_iso_str(
            unreliable_indicators.unreliable_oldest_vulnerability_report_date
        )
    if parent.creation:
        return get_as_str(parent.creation.modified_date)
    return None
