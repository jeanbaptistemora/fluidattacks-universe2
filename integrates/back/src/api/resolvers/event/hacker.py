from .schema import (
    EVENT,
)
from db_model.events.types import (
    Event,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@EVENT.field("hacker")
@enforce_group_level_auth_async
def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    analyst = parent.hacker
    return analyst
