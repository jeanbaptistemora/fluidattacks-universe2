from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> float:
    if "severity_threshold" in parent:
        return float(str(parent["severity_threshold"]))
    return 0.0
