from custom_types import (
    ForcesExecution,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: ForcesExecution, _info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    if "grace_period" in parent:
        return parent["grace_period"]
    return 0
