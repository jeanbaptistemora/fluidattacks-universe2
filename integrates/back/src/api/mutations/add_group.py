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
    get_key_or_fallback,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    description: str,
    organization: str,
    subscription: str = "continuous",
    language: str = "en",
    **parameters: Any,
) -> SimplePayloadType:
    # Compatibility with old API
    group_name = get_key_or_fallback(parameters)
    has_squad: bool = get_key_or_fallback(
        parameters, "has_squad", "has_drills", False
    )
    has_machine: bool = get_key_or_fallback(
        parameters, "has_machine", "has_skims", False
    )

    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    user_role = await authz.get_user_level_role(user_email)

    success = await groups_domain.add_group(
        user_email,
        user_role,
        group_name.lower(),
        organization,
        description,
        parameters.get(
            "service",
            ("WHITE" if subscription == "continuous" else "BLACK"),
        ),
        has_machine,
        has_squad,
        subscription,
        language,
    )

    if success:
        info.context.loaders.group.clear(group_name)
        await forces_domain.add_forces_user(info, group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created group {group_name.lower()} successfully",
        )

    return SimplePayloadType(success=success)
