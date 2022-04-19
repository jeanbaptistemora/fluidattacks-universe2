from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> Optional[str]:
    return parent.context
