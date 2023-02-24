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


@EVENT.field("solvingReason")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> EventSolutionReason | None:
    return (
        parent.state.reason
        if parent.state.status == EventStateStatus.SOLVED
        else None
    )
