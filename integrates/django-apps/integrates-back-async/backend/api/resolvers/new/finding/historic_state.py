# Standard
from typing import cast, Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    get_entity_cache_async,
    require_integrates
)
from backend.typing import Finding


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
@get_entity_cache_async
async def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Dict[str, str]]:
    historic_state: List[Dict[str, str]] = cast(
        Dict[str, List[Dict[str, str]]],
        parent
    )['historic_state']

    return historic_state
