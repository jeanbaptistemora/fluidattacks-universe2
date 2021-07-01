from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    resolve_kwargs,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    description: str,
    organization: str,
    subscription: str = "continuous",
    has_forces: bool = False,
    language: str = "en",
    **parameters: Any,
) -> SimplePayloadType:
    # Compatibility with old API
    group_name = resolve_kwargs(parameters)
    has_squad: bool = resolve_kwargs(
        parameters, "has_squad", "has_drills", False
    )
    has_machine: bool = resolve_kwargs(
        parameters, "has_machine", "has_skims", False
    )

    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    user_role = await authz.get_user_level_role(user_email)

    success = await groups_domain.create_group(
        user_email,
        user_role,
        group_name.lower(),
        organization,
        description,
        has_machine,
        has_squad,
        has_forces,
        subscription,
        language,
    )

    if success and has_forces:
        info.context.loaders.group.clear(group_name)
        await forces_domain.create_forces_user(info, group_name)
    if success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created group {group_name.lower()} successfully",
        )

    return SimplePayloadType(success=success)
