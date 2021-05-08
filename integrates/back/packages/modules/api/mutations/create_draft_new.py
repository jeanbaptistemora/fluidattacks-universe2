# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import SimplePayload
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from findings import domain as findings_domain
from newutils import logs as logs_utils


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    title: str,
    **kwargs: Any
) -> SimplePayload:
    await findings_domain.create_draft_new(
        info.context,
        group_name,
        title,
        **kwargs
    )
    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Created draft in {group_name} group successfully'
    )

    return SimplePayload(success=True)
