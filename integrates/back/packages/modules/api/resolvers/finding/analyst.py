
from typing import (
    Dict,
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
) -> str:
    analyst: str = cast(Dict[str, str], parent)['analyst']
    return analyst
