from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.events import (
    format_affected_components,
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
        if not parent["affected_components"]:
            return set()
        affected_components = format_affected_components(
            parent["affected_components"]
        )
    else:
        if not parent.affected_components:
            return set()
        affected_components = parent.affected_components

    return set(item.value for item in affected_components)
