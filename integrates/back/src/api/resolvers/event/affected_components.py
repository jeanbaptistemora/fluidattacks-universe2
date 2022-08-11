from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    _parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    return set()
