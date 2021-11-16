from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    Group as GroupType,
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
    validations as validations_utils,
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
        group_context = validations_utils.validate_markdown(
            kwargs.get("group_context", "")
        )
        validations_utils.validate_field_length(group_context, 20000)
        new_data: GroupType = {
            "group_context": group_context,
        }
        success = await groups_domain.update(group_name, new_data)
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to update group",
        )

    return SimplePayloadType(success=success)
