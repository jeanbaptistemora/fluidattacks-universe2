from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from db_model.roots.get import (
    get_git_environment_url_by_id,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
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
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, url_id: str, **_kwargs: Any
) -> Optional[GitEnvironmentUrl]:
    return await get_git_environment_url_by_id(url_id=url_id)
