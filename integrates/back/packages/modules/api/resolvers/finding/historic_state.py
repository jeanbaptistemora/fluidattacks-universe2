
from typing import (
    Dict,
    List,
    cast,
)

from graphql.type.definition import GraphQLResolveInfo

from custom_types import Finding
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
