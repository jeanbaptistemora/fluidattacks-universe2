from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
    add_root_environment_secret,
)
from typing import (
    Any,
)


@MUTATION.field("addGitEnvironmentSecret")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    __: GraphQLResolveInfo,
    key: str,
    value: str,
    url_id: str,
    description: str | None = None,
    **_kwargs: Any,
) -> SimplePayload:
    result = await add_root_environment_secret(url_id, key, value, description)

    return SimplePayload(success=result)
