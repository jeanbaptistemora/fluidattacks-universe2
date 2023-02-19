from .payloads.types import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
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
async def mutate(
    _: Any, info: GraphQLResolveInfo, remember: bool = False
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await stakeholders_domain.update_legal_remember(user_email, remember)

    return SimplePayload(success=True)
