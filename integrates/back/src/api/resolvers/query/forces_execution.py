from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.forces.types import (
    ForcesExecution,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.forces import (
    format_forces_to_resolve,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: str
) -> dict[str, Any]:
    response: dict[str, Any] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, _parent, _info, **kwargs),
        entity="forces_execution",
        attr="forces_execution",
        group=get_key_or_fallback(kwargs),
        id=kwargs["execution_id"],
    )
    return response


async def resolve_no_cache(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> dict[str, Any]:
    execution_id: str = kwargs["execution_id"]
    group_name: str = kwargs["group_name"]
    loaders: Dataloaders = info.context.loaders
    execution: ForcesExecution = await loaders.forces_execution.load(
        (group_name, execution_id)
    )
    return format_forces_to_resolve(execution=execution)
