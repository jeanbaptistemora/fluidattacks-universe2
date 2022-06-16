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
) -> str:
    event_status = str(parent["event_status"])

    return event_status
