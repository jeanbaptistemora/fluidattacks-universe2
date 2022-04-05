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
    add_secret,
)
from typing import (
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(  # pylint: disable=too-many-arguments
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    key: str,
    value: str,
    root_id: str,
    description: Optional[str] = None,
) -> SimplePayload:
    result = await add_secret(
        info.context.loaders, group_name, root_id, key, value, description
    )

    return SimplePayload(success=result)
