import authz
from db_model.groups.types import (
    Group,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[str]:
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    return sorted(await authz.get_group_service_attributes(group_name))
