from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
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
    **kwargs: Any,
) -> SimplePayload:
    success: bool = await findings_domain.create_draft(
        info, project_name, title, **kwargs
    )

    if success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created draft in {project_name} project successfully",
        )

    return SimplePayload(success=success)
