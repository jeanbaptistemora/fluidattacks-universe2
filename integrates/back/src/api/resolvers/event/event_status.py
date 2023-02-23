from .schema import (
    EVENT,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("eventStatus")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    event_status = parent.state.status.value
    return event_status
