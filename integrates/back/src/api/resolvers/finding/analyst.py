from custom_types import (
    Finding,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
)
from typing import (
    cast,
    Dict,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    hacker: str = get_key_or_fallback(
        cast(Dict[str, str], parent), "hacker", "analyst"
    )
    return hacker
