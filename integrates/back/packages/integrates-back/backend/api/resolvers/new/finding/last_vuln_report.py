# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import (
    finding as finding_domain,
)
from backend.typing import Finding


@get_entity_cache_async
async def resolve(
    parent: Dict[str, Finding],
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    finding_id: str = cast(str, parent['id'])
    last_vuln_report = cast(
        int,
        await finding_domain.get_finding_last_vuln_report(finding_id)
    )

    return last_vuln_report
