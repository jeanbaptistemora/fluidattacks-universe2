from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    ForcesExecution,
    ForcesExecutions,
)
from datetime import (
    datetime,
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
from newutils import (
    datetime as datetime_utils,
)
from newutils.utils import (
    get_key_or_fallback,
    get_present_key,
)
from typing import (
    Any,
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
) -> ForcesExecutions:
    # Compatibility with old API
    group_name: str = get_key_or_fallback(kwargs).lower()
    group_name_key: str = get_present_key(kwargs)
    from_date: datetime = kwargs.get(
        "from_date",
        datetime_utils.get_now_minus_delta(weeks=40, zone="UTC"),
    )
    to_date: datetime = kwargs.get(
        "to_date",
        datetime_utils.get_now(zone="UTC"),
    )

    executions: List[ForcesExecution] = []
    limit = 100
    counter = 0
    async for execution in forces_domain.get_executions(
        from_date=from_date,
        group_name=group_name,
        to_date=to_date,
        group_name_key=group_name_key,
    ):
        executions.append(execution)
        counter += 1
        if counter == limit:
            break

    return {
        "executions": executions,
        "from_date": from_date,
        f"{group_name_key}": group_name,
        "to_date": to_date,
    }
