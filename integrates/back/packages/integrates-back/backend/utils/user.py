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
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
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
    validate_field_length,
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
        phone_number = cast(str, invitation['phone_number'])
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

        if await user_domain.get_data(user_email, 'email'):
            success = success and await user_domain.add_phone_to_user(
                user_email,
                phone=phone_number
            )
        else:
            success = success and await user_domain.create(
                user_email,
                {
                    'phone': phone_number
                }
            )

        if not await user_domain.is_registered(user_email):
            success = success and all(await collect((
                user_domain.register(user_email),
                authz.grant_user_level_role(user_email, 'customer')
            )))

        if success:
            redis_del_by_deps_soon(
                'confirm_access',
                group_name=group_name,
                organization_id=organization_id,
            )

    return success


async def update_invited_stakeholder(
    updated_data: Dict[str, str],
    invitation: InvitationType,
    group_name: str
) -> bool:
    success = False
    email = updated_data['email']
    responsibility = updated_data['responsibility']
    phone_number = updated_data['phone_number']
    role = updated_data['role']
    new_invitation = invitation.copy()
    if (
        validate_field_length(responsibility, 50)
        and validate_alphanumeric_field(responsibility)
        and validate_phone_field(phone_number)
        and validate_email_address(email)
        and await validate_fluidattacks_staff_on_group(group_name, email, role)

    ):
        new_invitation['phone_number'] = phone_number
        new_invitation['responsibility'] = responsibility
        new_invitation['role'] = role

        success = await group_domain.update_access(
            email,
            group_name,
            {
                'invitation': new_invitation,

            }
        )

    return success


async def invite_to_group(  # pylint: disable=too-many-arguments
    context: Any,
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group_name: str,
) -> bool:
    success = False
    valid = (
        validate_alphanumeric_field(responsibility) and
        validate_phone_field(phone_number) and
        validate_email_address(email) and
        await validate_fluidattacks_staff_on_group(group_name, email, role)
    )
    if valid:
        if group_name and responsibility and len(responsibility) <= 50:
            now_str = datetime_utils.get_as_str(
                datetime_utils.get_now()
            )
            url_token = secrets.token_urlsafe(64)
            success = await group_domain.update_access(
                email,
                group_name,
                {
                    'has_access': False,
                    'invitation': {
                        'date': now_str,
                        'is_used': False,
                        'phone_number': phone_number,
                        'responsibility': responsibility,
                        'role': role,
                        'url_token': url_token,
                    },

                }
            )
            description = await group_domain.get_description(
                group_name.lower()
            )
            project_url = f'{BASE_URL}/confirm_access/{url_token}'
            mail_to = [email]
            email_context: MailContentType = {
                'admin': email,
                'project': group_name,
                'project_description': description,
                'project_url': project_url,
            }
            schedule(mailer.send_mail_access_granted(mail_to, email_context))
        else:
            util.cloudwatch_log(
                context,
                (f'Security: {email} Attempted to add responsibility '
                 f'to project {group_name} without validation')
            )

    return success


async def create_forces_user(
    info: GraphQLResolveInfo,
    group_name: str
) -> bool:
    user_email = user_domain.format_forces_user_email(group_name)
    success = await invite_to_group(
        context=info.context,
        email=user_email,
        responsibility='Forces service user',
        role='service_forces',
        phone_number='',
        group_name=group_name
    )

    # Give permissions directly, no confirmation required
    project_access = await group_domain.get_user_access(
        user_email, group_name
    )
    success = success and await complete_register_for_group_invitation(
        project_access
    )

    if not success:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={
                'extra': info.context,
                'username': group_name
            },
        )

    return success
