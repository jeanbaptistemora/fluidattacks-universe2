# Standard
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.filters import finding as finding_filters
from backend.typing import Finding


@get_entity_cache_async
async def resolve(
    parent: Dict[str, Finding],
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    release_date = finding_filters.get_approval_date(parent)

    return release_date
