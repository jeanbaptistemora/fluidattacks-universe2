# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import SimplePayload
from findings import domain as findings_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    project_name: str,
    title: str,
    **kwargs: Any
) -> SimplePayload:
    success: bool = await findings_domain.create_draft(
        info,
        project_name,
        title,
        **kwargs
    )

    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Created draft in {project_name} project successfully'
        )

    return SimplePayload(success=success)
