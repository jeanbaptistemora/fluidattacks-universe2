from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.utils import (
    get_key_or_fallback,
    get_present_key,
)
from typing import (
    Any,
    Dict,
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: Any
) -> Dict[str, Any]:
    # Compatibility with old API
    group_name: str = get_key_or_fallback(kwargs).lower()
    group_name_key: str = get_present_key(kwargs)

    executions: List[Dict[str, Any]] = []
    limit = 100
    counter = 0
    async for execution in forces_domain.get_executions(
        group_name=group_name,
        group_name_key=group_name_key,
    ):
        executions.append(execution)
        counter += 1
        if counter == limit:
            break

    return {
        "executions": executions,
        f"{group_name_key}": group_name,
    }
