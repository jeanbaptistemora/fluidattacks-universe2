# Standard
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import (
    finding as finding_domain,
)
from backend.typing import Finding
from backend.filters import finding as finding_filters


@get_entity_cache_async
async def resolve(
    parent: Dict[str, Finding],
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    release_date = finding_filters.get_approval_date(parent)

    return finding_domain.get_age_finding(release_date)
