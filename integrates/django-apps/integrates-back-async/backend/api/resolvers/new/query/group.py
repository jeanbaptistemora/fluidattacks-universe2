# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.domain import project as group_domain
from backend.typing import Project as Group


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> Group:
    name: str = kwargs['project_name']
    group: Group = await group_domain.get_by_name(name)

    return group
