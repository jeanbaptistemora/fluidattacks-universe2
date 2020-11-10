# Standard
import logging

# Third party
from aioextensions import schedule
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz, mailer, util
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login
)
from backend.domain import user as user_domain
from backend.typing import AddStakeholderPayload, MailContent
from fluidintegrates.settings import LOGGING


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
    phone_number: str = ''
) -> AddStakeholderPayload:
    success: bool = False
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    allowed_roles_to_grant = await authz.get_user_level_roles_a_user_can_grant(
        requester_email=user_email,
    )

    if role in allowed_roles_to_grant:
        new_user = await user_domain.create_without_project(
            email=email,
            role=role,
            phone_number=phone_number,
        )
        if new_user:
            util.cloudwatch_log(
                info.context,
                f'Security: Add stakeholder {email}'
            )
            mail_to = [email]
            context: MailContent = {'admin': email}
            schedule(mailer.send_mail_access_granted(mail_to, context))
            success = True
        else:
            LOGGER.error(
                'Error: Couldn\'t grant stakeholder access',
                extra={'extra': info.context})
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'email': email,
                    'requester_email': user_email,
                    'role': role
                }
            })
    return AddStakeholderPayload(success=success, email=email)
