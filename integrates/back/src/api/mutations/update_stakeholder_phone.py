from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from api.types import (
    APP_EXCEPTIONS,
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


@MUTATION.field("updateStakeholderPhone")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    phone: dict[str, str],
    verification_code: str,
    **_kwargs: Any,
) -> SimplePayload:
    try:
        user_info = await sessions_domain.get_jwt_content(info.context)
        user_email: str = user_info["user_email"]
        await stakeholders_domain.update_mobile(
            email=user_email,
            new_phone=StakeholderPhone(
                national_number=phone["national_number"],
                calling_country_code=phone["calling_country_code"],
                country_code="",
            ),
            verification_code=verification_code,
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

    return SimplePayload(success=True)
