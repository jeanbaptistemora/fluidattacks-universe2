# Standard
from typing import (
    Dict,
    List,
    cast,
)

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
) -> List[Dict[str, str]]:
    historic_state: List[Dict[str, str]] = cast(
        Dict[str, List[Dict[str, str]]],
        parent
    )['historic_state']

    return historic_state
