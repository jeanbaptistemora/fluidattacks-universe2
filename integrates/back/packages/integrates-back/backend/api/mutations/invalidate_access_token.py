# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import require_login
from backend.domain import user as user_domain
from backend.typing import SimplePayload as SimplePayloadType


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
) -> SimplePayloadType:
    user_info = await util.get_jwt_content(info.context)

    success = await user_domain.remove_access_token(
        user_info['user_email']
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} invalidate access token'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'{user_info["user_email"]} attempted to invalidate access token'
        )

    return SimplePayloadType(success=success)
