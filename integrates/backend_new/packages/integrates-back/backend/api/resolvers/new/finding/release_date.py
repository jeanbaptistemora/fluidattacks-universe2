# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.filters import finding as finding_filters
from backend.typing import Finding


@get_entity_cache_async
async def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    release_date = finding_filters.get_release_date(
        cast(Dict[str, Finding], parent)
    )

    return release_date
