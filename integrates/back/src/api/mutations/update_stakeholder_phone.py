from api import (
    APP_EXCEPTIONS,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Phone,
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    phone: Dict[str, str],
    verification_code: str,
    **_kwargs: Any,
) -> SimplePayloadType:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        await stakeholders_domain.update_mobile(
            user_email,
            Phone(
                national_number=phone["national_number"],
                calling_country_code=phone["calling_country_code"],
            ),
            verification_code,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated phone number for {user_email} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to update phone number for {user_email}",
        )
        raise

    return SimplePayloadType(success=True)
