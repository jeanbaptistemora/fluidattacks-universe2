from typing import Any

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload as SimplePayloadType
from newutils import token as token_utils
from users import domain as users_domain


@convert_kwargs_to_snake_case
async def mutate(
    _: Any, info: GraphQLResolveInfo, remember: bool = False
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    success = await users_domain.update_legal_remember(user_email, remember)

    return SimplePayloadType(success=success)
