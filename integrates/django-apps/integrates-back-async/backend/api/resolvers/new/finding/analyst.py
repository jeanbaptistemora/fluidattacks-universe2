# Standard
from typing import cast, Dict

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
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    # Temporary while migrating finding resolvers
    finding_id: str = cast(Dict[str, str], parent)['id']
    finding = await info.context.loaders['finding'].load(finding_id)

    analyst: str = cast(Dict[str, str], finding)['analyst']

    return analyst
