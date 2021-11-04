from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
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
from groups import (
    domain as groups_domain,
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
    require_asm,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> SimplePayloadType:
    group_name = group_name.lower()
    success = False

    try:
        success = await groups_domain.update_group_access_info(
            dast_access=kwargs.get("dast_access", ""),
            disambiguation=kwargs.get("disambiguation", ""),
            group_name=group_name,
            mobile_access=kwargs.get("mobile_access", ""),
            sast_access=kwargs.get("sast_access", ""),
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to update group",
        )

    return SimplePayloadType(success=success)
