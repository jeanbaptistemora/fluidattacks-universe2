from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)


@convert_kwargs_to_snake_case
@require_login
async def mutate(_parent: None, info: GraphQLResolveInfo) -> SimplePayload:
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await groups_domain.enroll_user_to_demo(user_email)
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: User {user_email} autoenrolled in demo group",
    )
    return SimplePayload(success=True)
