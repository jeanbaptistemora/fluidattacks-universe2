from aioextensions import (
    schedule,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_types import (
    AddStakeholderPayload,
    MailContent,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from mailer import (
    groups as groups_mail,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    email: str,
    role: str,
    phone_number: str = "",
) -> AddStakeholderPayload:
    success: bool = False
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    allowed_roles_to_grant = await authz.get_user_level_roles_a_user_can_grant(
        requester_email=user_email,
    )

    if role in allowed_roles_to_grant:
        new_user = await groups_domain.create_without_group(
            email=email,
            role=role,
            phone_number=phone_number,
        )
        if new_user:
            logs_utils.cloudwatch_log(
                info.context, f"Security: Added stakeholder {email}"
            )
            mail_to = [email]
            context: MailContent = {"admin": email}
            schedule(groups_mail.send_mail_access_granted(mail_to, context))
            success = True
        else:
            LOGGER.error(
                "Error: Couldn't grant stakeholder access",
                extra={"extra": info.context},
            )
    else:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "email": email,
                    "requester_email": user_email,
                    "role": role,
                }
            },
        )
    return AddStakeholderPayload(success=success, email=email)
