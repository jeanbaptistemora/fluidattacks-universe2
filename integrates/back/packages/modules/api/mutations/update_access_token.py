# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend.typing import (
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType
)
from custom_exceptions import InvalidExpirationTime
from decorators import require_login
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from users import domain as users_domain


@convert_kwargs_to_snake_case
@require_login
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    expiration_time: int
) -> UpdateAccessTokenPayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    email = user_info['user_email']
    try:
        result = await users_domain.update_access_token(
            email,
            expiration_time,
            first_name=user_info['first_name'],
            last_name=user_info['last_name']
        )
        if result.success:
            logs_utils.cloudwatch_log(
                info.context,
                f'{user_info["user_email"]} update access token'
            )
        else:
            logs_utils.cloudwatch_log(
                info.context,
                f'{user_info["user_email"]} attempted to update access token'
            )
        return result
    except InvalidExpirationTime as exception:
        logs_utils.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to use expiration time '
            f'greater than six months or minor than current time'
        )
        raise exception
