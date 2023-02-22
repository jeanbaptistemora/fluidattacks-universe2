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
from graphql import (
    GraphQLResolveInfo,
)


@EVENT.field("otherSolvingReason")
async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str | None:
    return (
        parent.state.other
        if parent.state.status == EventStateStatus.SOLVED
        and parent.state.reason == EventSolutionReason.OTHER
        else None
    )
