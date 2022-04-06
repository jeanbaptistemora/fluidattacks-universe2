from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    validate_new_invitation_time_limit,
)
from newutils import (
    token as token_utils,
)
from remove_user.domain import (
    confirm_deletion_mail,
    get_confirm_deletion,
)
from typing import (
    Any,
)


@require_login
async def mutate(_: Any, info: GraphQLResolveInfo) -> SimplePayloadType:
    stakeholder_info = await token_utils.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    deletion = await get_confirm_deletion(email=stakeholder_email)

    if deletion:
        if "expiration_time" in deletion:
            validate_new_invitation_time_limit(
                int(deletion["expiration_time"])
            )

    success = await confirm_deletion_mail(email=stakeholder_email)

    return SimplePayloadType(success=success)
