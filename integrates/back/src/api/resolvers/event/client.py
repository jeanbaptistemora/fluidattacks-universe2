from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], Event],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    if isinstance(parent, dict):
        client = str(parent["client"])
    else:
        client = parent.client
    return client
