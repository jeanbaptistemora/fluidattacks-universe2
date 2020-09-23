# Standard
from typing import List

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import project as group_domain


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **_kwargs: str
) -> List[str]:
    return await group_domain.get_alive_projects()
