from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)


async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> Optional[str]:
    if isinstance(parent, dict):
        return parent["service"]

    if parent.state.service:
        return parent.state.service.value
    return None
