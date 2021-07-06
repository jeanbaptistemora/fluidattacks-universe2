from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
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
from newutils.utils import (
    clean_up_kwargs,
    resolve_kwargs,
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
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    title: str,
    **kwargs: Any,
) -> SimplePayload:
    # Compatibility with old API
    group_name: str = resolve_kwargs(kwargs)
    kwargs = clean_up_kwargs(kwargs)

    success: bool = await findings_domain.create_draft(
        info, group_name, title, **kwargs
    )

    if success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created draft in {group_name} group successfully",
        )

    return SimplePayload(success=success)
