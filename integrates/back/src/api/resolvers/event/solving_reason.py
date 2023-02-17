from .schema import (
    EVENT,
)
from db_model.events.enums import (
    EventSolutionReason,
    EventStateStatus,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@EVENT.field("solvingReason")
async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[EventSolutionReason]:
    return (
        parent.state.reason
        if parent.state.status == EventStateStatus.SOLVED
        else None
    )
