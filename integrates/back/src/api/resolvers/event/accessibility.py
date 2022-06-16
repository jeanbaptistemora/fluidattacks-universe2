from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.events import (
    format_accessibility,
)
from typing import (
    Any,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], Event],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    if isinstance(parent, dict):
        if not parent["accessibility"]:
            return set()
        accessibility = format_accessibility(parent["accessibility"])
    else:
        if not parent.accessibility:
            return set()
        accessibility = parent.accessibility

    return set(item.value for item in accessibility)
