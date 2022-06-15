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
    access: set[str] = (
        set(str(parent["accessibility"]).split())
        if parent["affected_components"]
        else set()
    )
    return access
