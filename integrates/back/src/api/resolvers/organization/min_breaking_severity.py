from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: Dict[str, str],
) -> float:
    if "min_breaking_severity" in parent:
        return parent["min_breaking_severity"]
    return 0.0
