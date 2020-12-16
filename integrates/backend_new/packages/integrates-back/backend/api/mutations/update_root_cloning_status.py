# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_login,
)
from backend.domain import root as root_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@rename_kwargs({'id': 'root_id'})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
@rename_kwargs({'root_id': 'id'})
async def mutate(
    _: None,
    __: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:

    await root_domain.update_root_cloning_status(
        kwargs['id'],
        kwargs['status'],
        kwargs['reason'],
    )

    return SimplePayload(success=True)
