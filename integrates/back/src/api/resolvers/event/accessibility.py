from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[set[str]]:
    access: set[str] = set(str(parent["accessibility"]).split())

    return access
