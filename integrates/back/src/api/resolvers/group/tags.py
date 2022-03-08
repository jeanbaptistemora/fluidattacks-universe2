from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)


async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> Optional[List[str]]:
    if isinstance(parent, dict):
        return parent["tags"]

    return list(parent.tags) if parent.tags else None
