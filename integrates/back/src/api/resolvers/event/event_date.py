from .schema import (
    EVENT,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_as_str,
)


@EVENT.field("eventDate")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    return get_as_str(parent.event_date)
