# Standard library
from typing import Any

# Third party libraries

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.typing import SimplePayload as SimplePayloadType
from users import domain as users_domain


@convert_kwargs_to_snake_case  # type: ignore
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    token: str
) -> SimplePayloadType:
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    success = await users_domain.add_push_token(user_email, token)

    return SimplePayloadType(success=success)
