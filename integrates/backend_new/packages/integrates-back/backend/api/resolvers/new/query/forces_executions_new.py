# Standard
from datetime import datetime
from typing import Any, List

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
from backend.domain import forces as forces_domain
from backend.typing import ForcesExecution, ForcesExecutions
from backend.util import datetime_utils


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: Any
) -> ForcesExecutions:
    group_name: str = kwargs['project_name'].lower()
    from_date: datetime = kwargs.get(
        'from_date',
        datetime_utils.get_now_minus_delta(weeks=1, timezone='UTC'),
    )
    to_date: datetime = kwargs.get(
        'to_date',
        datetime_utils.get_now(timezone='UTC'),
    )

    executions: List[ForcesExecution] = await forces_domain.get_executions_new(
        from_date=from_date,
        group_name=group_name,
        to_date=to_date
    )

    return {
        'executions': executions,
        'from_date': from_date,
        'project_name': group_name,
        'to_date': to_date
    }
