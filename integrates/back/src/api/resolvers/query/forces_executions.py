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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.forces import (
    format_forces_to_resolve,
)
from newutils.utils import (
    get_key_or_fallback,
    get_present_key,
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
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> dict[str, Any]:
    # Compatibility with old API
    group_name: str = get_key_or_fallback(kwargs).lower()
    group_name_key: str = get_present_key(kwargs)
    loaders: Dataloaders = info.context.loaders

    executions_typed: tuple[
        ForcesExecution, ...
    ] = await loaders.forces_executions.load((group_name, 100))
    executions = [
        format_forces_to_resolve(execution) for execution in executions_typed
    ]
    return {
        "executions": executions,
        f"{group_name_key}": group_name,
    }
