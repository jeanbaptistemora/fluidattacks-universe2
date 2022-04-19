from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    return str(parent.state.tier.value).lower()
