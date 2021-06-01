from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
)
from users import (
    domain as users_domain,
)


@convert_kwargs_to_snake_case
async def mutate(
    _: Any, info: GraphQLResolveInfo, token: str
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    success = await users_domain.add_push_token(user_email, token)

    return SimplePayloadType(success=success)
