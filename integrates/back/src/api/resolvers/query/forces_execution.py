from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    ForcesExecution,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from forces import (
    domain as forces_domain,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: str
) -> ForcesExecution:
    response: ForcesExecution = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, _parent, _info, **kwargs),
        entity="forces_execution",
        attr="forces_execution",
        group=get_key_or_fallback(kwargs),
        id=kwargs["execution_id"],
    )
    return response


async def resolve_no_cache(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: str
) -> ForcesExecution:
    execution_id: str = kwargs["execution_id"]
    group_name: str = get_key_or_fallback(kwargs)
    return await forces_domain.get_execution(
        execution_id=execution_id, group_name=group_name.lower()
    )
