# Standard
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.filters import finding as finding_filters
from backend.typing import Finding


async def resolve(
    parent: Dict[str, Finding],
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    report_date = ''
    is_finding_created = finding_filters.is_created(parent)

    if is_finding_created:
        report_date = finding_filters.get_creation_date(parent)
    else:
        report_date = finding_filters.get_submission_date(parent)

    return report_date
