# Standard
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Finding
from decorators import enforce_group_level_auth_async


@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    analyst: str = cast(Dict[str, str], parent)['analyst']

    return analyst
