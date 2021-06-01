from custom_types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
    Dict,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    analyst: str = cast(Dict[str, str], parent)["analyst"]
    return analyst
