from db_model.events.types import (
    Event,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


async def resolve(
    parent: Event,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> set[str]:
    if not parent.affected_components:
        return set()
    affected_components = parent.affected_components

    return set(item.value for item in affected_components)
