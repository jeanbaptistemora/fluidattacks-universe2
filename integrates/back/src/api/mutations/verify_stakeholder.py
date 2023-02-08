from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from db_model.stakeholders.types import (
    StakeholderPhone,
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
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
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
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayloadType:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    new_phone_dict = kwargs.get("new_phone")
    new_phone = None
    if new_phone_dict:
        new_phone = StakeholderPhone(
            calling_country_code=new_phone_dict["calling_country_code"],
            national_number=new_phone_dict["national_number"],
            country_code="",
        )

    try:
        await stakeholders_domain.verify(
            info.context.loaders,
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
