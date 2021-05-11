
from typing import (
    List,
    cast,
)

from graphql.type.definition import GraphQLResolveInfo

import authz
from custom_types import Project as Group
from decorators import enforce_group_level_auth_async


@enforce_group_level_auth_async
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[str]:
    group_name: str = cast(str, parent['name'])
    return sorted(await authz.get_group_service_attributes(group_name))
