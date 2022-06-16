from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.events import (
    format_accessibility_item,
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
        access: set[str] = (
            set(str(parent["accessibility"]).split())
            if parent["affected_components"]
            else set()
        )
    else:
        access = (
            set(format_accessibility_item(parent.accessibility).split(" "))
            if parent.accessibility
            else set()
        )
    return access
