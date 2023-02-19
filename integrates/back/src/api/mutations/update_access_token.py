from .payloads.types import (
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidExpirationTime,
    UnavailabilityError,
)
from decorators import (
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
@require_login
async def mutate(
    _: Any, info: GraphQLResolveInfo, expiration_time: int
) -> UpdateAccessTokenPayloadType:
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]
    try:
        result = await stakeholders_domain.update_access_token(
            email,
            expiration_time,
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
        )
        logs_utils.cloudwatch_log(
            info.context, f'{user_info["user_email"]} update access token'
        )
        return UpdateAccessTokenPayloadType(success=True, session_jwt=result)
    except UnavailabilityError:
        logs_utils.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to update access token',
        )
        return UpdateAccessTokenPayloadType(success=False, session_jwt=result)
    except InvalidExpirationTime as exception:
        logs_utils.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to use expiration time '
            f"greater than six months or minor than current time",
        )
        raise exception
