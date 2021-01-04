# Standard
from typing import cast, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import project as group_domain


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[str]:
    return cast(List[str], await group_domain.get_alive_projects())
