from custom_types import (
    ForcesExecution,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: ForcesExecution, _info: GraphQLResolveInfo, **_kwargs: None
) -> float:
    if "severity_threshold" in parent:
        return parent["severity_threshold"]
    return 0.0
