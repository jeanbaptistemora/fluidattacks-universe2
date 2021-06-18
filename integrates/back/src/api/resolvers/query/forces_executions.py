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
    require_integrates,
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
    resolve_kwargs,
    resolve_kwargs_key,
)
from typing import (
    Any,
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: Any
) -> ForcesExecutions:
    # Compatibility with old API
    group_name: str = resolve_kwargs(kwargs).lower()
    group_name_key: str = resolve_kwargs_key(kwargs)
    from_date: datetime = kwargs.get(
        "from_date",
        datetime_utils.get_now_minus_delta(weeks=1, zone="UTC"),
    )
    to_date: datetime = kwargs.get(
        "to_date",
        datetime_utils.get_now(zone="UTC"),
    )

    executions: List[ForcesExecution] = await forces_domain.get_executions(
        from_date=from_date,
        group_name=group_name,
        to_date=to_date,
        group_name_key=group_name_key,
    )
    return {
        "executions": executions,
        "from_date": from_date,
        f"{group_name_key}": group_name,
        "to_date": to_date,
    }
