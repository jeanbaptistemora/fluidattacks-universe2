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
from typing import (
    Any,
)
from users import (
    domain as users_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayloadType:
    try:
        user_info = await token_utils.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        new_phone_dict = kwargs.get("new_phone")
        new_phone = None
        if new_phone_dict:
            new_phone = Phone(
                calling_country_code=new_phone_dict["calling_country_code"],
                national_number=new_phone_dict["national_number"],
            )

        await users_domain.verify(
            user_email,
            new_phone,
            kwargs.get("verification_code"),
        )

        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Verified {user_email} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to verify {user_email}",
        )
        raise

    return SimplePayloadType(success=True)
