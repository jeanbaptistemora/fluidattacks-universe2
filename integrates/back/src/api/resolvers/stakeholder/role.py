from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
    Union,
)


async def resolve(
    parent: Union[dict[str, Any], Stakeholder],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    if isinstance(parent, dict):
        role = parent.get("role", None)
    else:
        role = parent.role
    return role
