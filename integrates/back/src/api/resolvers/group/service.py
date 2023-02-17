from .schema import (
    GROUP,
)
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@GROUP.field("service")
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
) -> Optional[str]:
    if parent.state.service:
        return parent.state.service.value
    return None
