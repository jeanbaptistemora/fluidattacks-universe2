# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.typing import Finding


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    finding_id: str = cast(Dict[str, str], parent)['id']
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    return cast(str, finding['sorts'])
