# Standard library
import logging
from typing import (
    Any,
    Awaitable,
    List
)

# Third party libraries
from aioextensions import (
    collect,
    schedule
)
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING

from backend import (
    authz,
    mailer,
    util
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import (
    organization as org_domain,
    project as project_domain,
    user as user_domain
)
from backend.typing import (
    GrantStakeholderAccessPayload as GrantStakeholderAccessPayloadType,
    MailContent as MailContentType
)
from backend.utils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_fluidattacks_staff_on_group,
    validate_phone_field
)

from __init__ import BASE_URL

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _give_user_access(
    email: str,
    group: str,
    responsibility: str,
    phone_number: str
) -> bool:
    success = False
    coroutines: List[Awaitable[bool]] = []

    if phone_number and phone_number[1:].isdigit():
        coroutines.append(
            user_domain.add_phone_to_user(email, phone_number)
        )

    if group and all(await collect(coroutines)):
        urltoken = await util.create_confirm_access_token(
            email, group, responsibility
        )
        description = await project_domain.get_description(
            group.lower()
        )
        project_url = f'{BASE_URL}/confirm_access/{urltoken}'
        mail_to = [email]
        context: MailContentType = {
            'admin': email,
            'project': group,
            'project_description': description,
            'project_url': project_url,
        }
        schedule(mailer.send_mail_access_granted(mail_to, context))
        success = True

    return success


async def _create_new_user(  # pylint: disable=too-many-arguments
    context: Any,
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group: str,
) -> bool:
    valid = (
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group, email, role)
    )
    success_granted = False
    success_access_given = False
    if valid:
        success_granted = await authz.grant_group_level_role(
            email, group, role
        )

        if not await user_domain.get_data(email, 'email'):
            await user_domain.create(
                email.lower(),
                {
                    'phone': phone_number
                }
            )

        organization_id = await org_domain.get_id_for_group(group)
        if not await org_domain.has_user_access(organization_id, email):
            await org_domain.add_user(organization_id, email, 'customer')

        if not await user_domain.is_registered(email):
            await collect((
                user_domain.register(email),
                authz.grant_user_level_role(email, 'customer')
            ))

        if group and responsibility and len(responsibility) <= 50:
            success_access_given = await _give_user_access(
                email,
                group,
                responsibility,
                phone_number
            )
        else:
            util.cloudwatch_log(
                context,
                (f'Security: {email} Attempted to add responsibility '
                 f'to project {group} without validation')  # pragma: no cover
            )

    return success_granted and success_access_given


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    role: str,
    **query_args: str
) -> GrantStakeholderAccessPayloadType:
    project_name = query_args.get('project_name', '').lower()
    success = False
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    new_user_role = role
    new_user_email = query_args.get('email', '')

    allowed_roles_to_grant = \
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )

    if new_user_role in allowed_roles_to_grant:
        if await _create_new_user(
                context=info.context,
                email=new_user_email,
                responsibility=query_args.get('responsibility', '-'),
                role=new_user_role,
                phone_number=query_args.get('phone_number', ''),
                group=project_name):
            success = True
        else:
            LOGGER.error(
                'Couldn\'t grant access to project',
                extra={'extra': info.context}
            )
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'new_user_role': new_user_role,
                    'project_name': project_name,
                    'requester_email': user_email
                }
            }
        )

    if success:
        util.queue_cache_invalidation(
            f'stakeholders*{project_name}',
            new_user_email
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Given grant access to {new_user_email} '
            f'in {project_name} project'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to grant access to {new_user_email} '
            f'in {project_name} project'
        )

    return GrantStakeholderAccessPayloadType(
        success=success,
        granted_stakeholder=dict(
            project_name=project_name,
            email=new_user_email
        )
    )
