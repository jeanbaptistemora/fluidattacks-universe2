from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from roots.domain import (
    remove_environment_url_secret,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None, __: GraphQLResolveInfo, key: str, url_id: str, **_kwargs: Any
) -> SimplePayload:
    await remove_environment_url_secret(url_id, key)

    return SimplePayload(success=True)
