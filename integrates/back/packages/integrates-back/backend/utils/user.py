# Standard libraries
import logging
import secrets
from typing import (
    Any,
    Awaitable,
    Dict,
    List,
    cast
)

# Third party libraries
import bugsnag
from aioextensions import (
    collect,
    schedule
)

from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING

from backend import (
    authz,
    mailer,
    util
)
from backend.domain import (
    organization as org_domain,
    project as group_domain,
    user as user_domain
)
from backend.typing import (
    Invitation as InvitationType,
    MailContent as MailContentType,
    ProjectAccess as ProjectAccessType,
)
from backend.utils import (
    datetime as datetime_utils,
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


async def _add_acess(
    responsibility: str,
    email: str,
    project_name: str,
    context: object
) -> bool:
    result = False
    if len(responsibility) <= 50:
        result = await group_domain.update_access(
            email,
            project_name,
            {
                'responsibility': responsibility
            }
        )
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to add responsibility to '
            f'project{project_name} bypassing validation'
        )

    return result


async def modify_user_information(
    context: Any,
    modified_user_data: Dict[str, str],
    project_name: str
) -> bool:
    success = False
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    coroutines: List[Awaitable[bool]] = []

    if responsibility:
        coroutines.append(_add_acess(
            responsibility,
            email,
            project_name,
            context
        ))

    if phone and validate_phone_field(phone):
        coroutines.append(
            user_domain.add_phone_to_user(email, phone)
        )
        success = all(await collect(coroutines))
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to edit '
            f'user phone bypassing validation'
        )

    return success


async def complete_register_for_group_invitation(
    project_access: ProjectAccessType
) -> bool:
    success = False
    invitation = cast(InvitationType, project_access['invitation'])

    if invitation['is_used']:
        bugsnag.notify(Exception('Token already used'), severity='warning')
    else:
        user_email = cast(str, project_access['user_email'])
        group_name = cast(str, project_access['project_name'])
        updated_invitation = invitation.copy()
        updated_invitation['is_used'] = True
        responsibility = cast(str, invitation['responsibility'])
        role = cast(str, invitation['role'])
        success = await group_domain.update_access(
            user_email,
            group_name,
            {
                'has_access': True,
                'invitation': updated_invitation,
                'responsibility': responsibility,
            }
        )

        success = success and await authz.grant_group_level_role(
            user_email, group_name, role
        )

        organization_id = await org_domain.get_id_for_group(group_name)
        if not await org_domain.has_user_access(organization_id, user_email):
            success = success and await org_domain.add_user(
                organization_id,
                user_email,
                'customer'
            )

        if not await user_domain.is_registered(user_email):
            success = success and all(await collect((
                user_domain.register(user_email),
                authz.grant_user_level_role(user_email, 'customer')
            )))

    return success


async def _give_user_access(
    email: str,
    group: str,
    responsibility: str,
    role: str,
    phone_number: str
) -> bool:
    success = False
    coroutines: List[Awaitable[bool]] = []

    if phone_number and phone_number[1:].isdigit():
        coroutines.append(
            user_domain.add_phone_to_user(email, phone_number)
        )

    if group and all(await collect(coroutines)):
        now_str = datetime_utils.get_as_str(
            datetime_utils.get_now()
        )
        url_token = secrets.token_urlsafe(64)
        await group_domain.update_access(
            email,
            group,
            {
                'invitation': {
                    'date': now_str,
                    'is_used': False,
                    'responsibility': responsibility,
                    'role': role,
                    'url_token': url_token,
                },

            }
        )
        description = await group_domain.get_description(
            group.lower()
        )
        project_url = f'{BASE_URL}/confirm_access/{url_token}'
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


async def create_new_user(  # pylint: disable=too-many-arguments
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
                role,
                phone_number
            )
        else:
            util.cloudwatch_log(
                context,
                (f'Security: {email} Attempted to add responsibility '
                 f'to project {group} without validation')  # pragma: no cover
            )

    return success_granted and success_access_given


async def create_forces_user(
    info: GraphQLResolveInfo,
    group_name: str
) -> bool:
    user_email = user_domain.format_forces_user_email(group_name)
    success = await create_new_user(
        context=info.context,
        email=user_email,
        responsibility='Forces service user',
        role='service_forces',
        phone_number='',
        group=group_name
    )

    # Give permissions directly, no confirmation required
    success = success and await group_domain.update_has_access(
        user_email, group_name, True)
    success = success and await authz.grant_group_level_role(
        user_email, group_name, 'service_forces')

    if not success:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={
                'extra': info.context,
                'username': group_name
            },
        )

    return success
