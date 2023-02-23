from .schema import (
    EVENT,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("id")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    event_id = parent.id
    return event_id
