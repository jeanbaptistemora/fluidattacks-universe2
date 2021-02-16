# Standard

# Third party
from typing import (
    cast,
    Optional,
)
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.domain import forces as forces_domain
from backend.typing import Project as Group


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    parent: Group,
    __: GraphQLResolveInfo,
) -> Optional[str]:
    group_name: str = cast(str, parent['name'])
    token: Optional[str] = await forces_domain.get_token(group_name)

    return token
