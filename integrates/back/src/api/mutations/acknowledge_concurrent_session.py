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
from stakeholders import (
    domain as stakeholders_domain,
)


@convert_kwargs_to_snake_case
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
) -> SimplePayloadType:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await stakeholders_domain.acknowledge_concurrent_session(user_email)

    return SimplePayloadType(success=True)
