from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
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


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: Any,
) -> Optional[str]:
    if isinstance(parent, dict):
        return parent.get("agent_token")

    return parent.agent_token
