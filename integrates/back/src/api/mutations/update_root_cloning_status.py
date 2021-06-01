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
from roots import (
    domain as roots_domain,
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
    _: None,
    __: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:

    await roots_domain.update_root_cloning_status(
        kwargs["group_name"],
        kwargs["id"],
        kwargs["status"],
        kwargs["message"],
    )

    return SimplePayload(success=True)
