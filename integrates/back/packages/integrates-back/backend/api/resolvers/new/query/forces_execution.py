# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    get_entity_cache_async,
    require_integrates,
    require_login,
)
from backend.domain import forces as forces_domain
from backend.typing import ForcesExecution


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
@get_entity_cache_async
async def resolve(
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
