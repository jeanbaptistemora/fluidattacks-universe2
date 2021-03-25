# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import require_login
from backend.exceptions import InvalidExpirationTime
from backend.typing import (
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType
)
from users import domain as users_domain


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    expiration_time: int
) -> UpdateAccessTokenPayloadType:
    user_info = await util.get_jwt_content(info.context)
    email = user_info['user_email']
    try:
        result = await users_domain.update_access_token(
            email,
            expiration_time,
            first_name=user_info['first_name'],
            last_name=user_info['last_name']
        )
        if result.success:
            util.cloudwatch_log(
                info.context,
                f'{user_info["user_email"]} update access token'
            )
        else:
            util.cloudwatch_log(
                info.context,
                f'{user_info["user_email"]} attempted to update access token'
            )
        return result
    except InvalidExpirationTime as exception:
        util.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to use expiration time '
            f'greater than six months or minor than current time'
        )
        raise exception
