# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    enforce_group_level_auth_async,
    get_entity_cache_async
)
from backend.typing import Finding


@enforce_group_level_auth_async
@get_entity_cache_async
async def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    analyst: str = cast(Dict[str, str], parent)['analyst']

    return analyst
