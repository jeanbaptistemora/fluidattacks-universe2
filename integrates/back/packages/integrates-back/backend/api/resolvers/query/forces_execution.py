# Standard
from functools import (
    partial,
)

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.domain import forces as forces_domain
from backend.typing import ForcesExecution


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> ForcesExecution:
    response: ForcesExecution = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, _parent, _info, **kwargs),
        entity='forces_execution',
        attr='forces_execution',
        group=kwargs['project_name'],
        id=kwargs['execution_id'],
    )

    return response


async def resolve_no_cache(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> ForcesExecution:
    execution_id: str = kwargs['execution_id']
    project_name: str = kwargs['project_name']

    return await forces_domain.get_execution(
        execution_id=execution_id,
        group_name=project_name.lower()
    )
