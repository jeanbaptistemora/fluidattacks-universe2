from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    affected_components: set[str] = (
        set(str(parent["affected_components"]).split("\n"))
        if parent["affected_components"]
        else set()
    )
    return affected_components
