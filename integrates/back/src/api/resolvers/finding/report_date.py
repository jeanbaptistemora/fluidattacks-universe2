from custom_types import (
    Finding,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    findings as findings_utils,
)
from typing import (
    Dict,
)


async def resolve(
    parent: Dict[str, Finding], _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    report_date = (
        findings_utils.get_creation_date(parent)
        if findings_utils.is_created(parent)
        else findings_utils.get_submission_date(parent)
    )
    return report_date
