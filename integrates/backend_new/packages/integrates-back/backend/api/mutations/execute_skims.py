# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.domain import skims as skims_domain
from backend.typing import ExecuteSkimsPayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: None,
    __: GraphQLResolveInfo,
    group_name: str,
    **___: Any,
) -> ExecuteSkimsPayload:
    result = await skims_domain.execute_skims(group_name.lower())
    return ExecuteSkimsPayload(success=result[0], pipeline_url=result[1])
