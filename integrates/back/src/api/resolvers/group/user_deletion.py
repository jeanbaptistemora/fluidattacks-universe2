from db_model.groups.enums import (
    GroupStateStatus,
)
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
        return parent["user_deletion"]

    return (
        parent.state.modified_by
        if parent.state.status == GroupStateStatus.DELETED
        else None
    )
