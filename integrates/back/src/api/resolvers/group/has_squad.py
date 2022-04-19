from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> bool:
    return parent.state.has_squad
