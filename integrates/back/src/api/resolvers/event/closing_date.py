from db_model.events.enums import (
    EventStateStatus,
)
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
        closing_date = str(parent["closing_date"])
    else:
        if parent.state.status == EventStateStatus.SOLVED:
            closing_date = parent.state.modified_date
        else:
            closing_date = ""
    return closing_date
