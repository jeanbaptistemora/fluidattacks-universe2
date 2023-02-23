from .schema import (
    EVENT,
)
from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("detail")
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    detail = parent.description

    return detail
