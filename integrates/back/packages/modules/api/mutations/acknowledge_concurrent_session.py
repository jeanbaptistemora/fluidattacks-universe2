# Standard library
from typing import Any

# Third party libraries

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend.typing import SimplePayload as SimplePayloadType
from newutils import token as token_utils
from users import domain as users_domain


@convert_kwargs_to_snake_case
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info['user_email']
    success = await users_domain.acknowledge_concurrent_session(user_email)

    return SimplePayloadType(success=success)
