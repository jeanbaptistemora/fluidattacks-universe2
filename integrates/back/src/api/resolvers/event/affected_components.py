from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.events import (
    format_affected_components_item,
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
        affected_components: set[str] = (
            set(str(parent["affected_components"]).split("\n"))
            if parent["affected_components"]
            else set()
        )
    else:
        affected_components = (
            set(
                format_affected_components_item(
                    parent.affected_components
                ).split("\n")
            )
            if parent.affected_components
            else set()
        )
    return affected_components
