# pylint: disable=too-many-locals
from typing import Dict, List
import sys
import threading

from asgiref.sync import sync_to_async
from backend.api.dataloaders import user as user_loader
from backend.decorators import (
    require_login, require_project_access,
    enforce_group_level_auth_async,
    enforce_user_level_auth_async,
)
from backend.domain import project as project_domain, user as user_domain
from backend.mailer import send_mail_access_granted
from backend.typing import (
    User as UserType,
    AddUserPayload as AddUserPayloadType,
    GrantUserAccessPayload as GrantUserAccessPayloadType,
    RemoveUserAccessPayload as RemoveUserAccessPayloadType,
    EditUserPayload as EditUserPayloadType,
)
from backend import util
from backend.utils import authorization as authorization_utils
from backend.utils.validations import (
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)

import rollbar

from ariadne import convert_kwargs_to_snake_case

# Constants
BASIC_ROLES = ['customer', 'customeradmin']
INTERNAL_ROLES = ['admin', 'analyst']


# pylint: disable=too-many-arguments
@sync_to_async
def _create_new_user(context: object, email: str, organization: str,
                     responsibility: str, role: str, phone_number: str,
                     group: str) -> bool:
    valid = validate_alphanumeric_field(organization) \
        and validate_alphanumeric_field(responsibility) \
        and validate_alphanumeric_field(role) \
        and validate_phone_field(phone_number) \
        and validate_email_address(email)

    if not valid:
        return False

    success = user_domain.grant_group_level_role(email, group, role)

    if not user_domain.get_data(email, 'email'):
        user_domain.create(email.lower(), {
            'company': organization.lower(),
            'phone': phone_number
        })

    if not user_domain.is_registered(email):
        user_domain.register(email)
        user_domain.grant_user_level_role(email, 'customer')
        user_domain.update(email, organization.lower(), 'company')

    if group and responsibility and len(responsibility) <= 50:
        project_domain.add_access(
            email, group, 'responsibility', responsibility)
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to add responsibility to project '
            '{group} without validation')  # pragma: no cover
        return False

    if phone_number and phone_number[1:].isdigit():
        user_domain.add_phone_to_user(email, phone_number)

    if group and user_domain.update_project_access(email, group, True):
        description = project_domain.get_description(group.lower())
        project_url = \
            'https://fluidattacks.com/integrates/dashboard#!/project/' \
            + group.lower() + '/indicators'
        mail_to = [email]
        context = {
            'admin': email,
            'project': group,
            'project_description': description,
            'project_url': project_url,
        }
        email_send_thread = \
            threading.Thread(name='Access granted email thread',
                             target=send_mail_access_granted,
                             args=(mail_to, context,))
        email_send_thread.start()
        success = True
    return success


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
async def resolve_user(
        _, info, project_name: str, user_email: str) -> UserType:
    """Resolve user query."""
    return await user_loader.resolve(info, user_email, project_name)


@convert_kwargs_to_snake_case
async def resolve_user_mutation(obj, info, **parameters):
    """Wrap user mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


@require_login
@enforce_user_level_auth_async
async def _do_add_user(_, info, **parameters) -> AddUserPayloadType:
    """Resolve add_user mutation."""
    email = parameters.get('email', '')
    success = \
        await sync_to_async(user_domain.create_without_project)(parameters)
    if success:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Add user {email}')  # pragma: no cover
        mail_to = [email]
        context = {'admin': email}
        email_send_thread = threading.Thread(
            name='Access granted email thread',
            target=send_mail_access_granted,
            args=(mail_to, context,)
        )
        email_send_thread.start()
    return AddUserPayloadType(success=success, email=email)


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_grant_user_access(
        _, info, **query_args) -> GrantUserAccessPayloadType:
    """Resolve grant_user_access mutation."""
    project_name = query_args.get('project_name', '').lower()
    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    new_user_role = query_args.get('role')
    new_user_email = query_args.get('email', '')

    enforcer = authorization_utils.get_group_level_enforcer_async(user_email)
    if enforcer.enforce(user_email, project_name,
                        'backend_api_resolvers_user'
                        '__do_grant_user_access_internal_roles'):
        allowed_roles_to_grant = BASIC_ROLES + INTERNAL_ROLES
    else:
        allowed_roles_to_grant = BASIC_ROLES

    if new_user_role in allowed_roles_to_grant:
        if await _create_new_user(
                context=info.context,
                email=new_user_email,
                organization=query_args.get('organization', ''),
                responsibility=query_args.get('responsibility', '-'),
                role=query_args.get('role', ''),
                phone_number=query_args.get('phone_number', ''),
                group=project_name):
            success = True
        else:
            rollbar.report_message('Error: Couldn\'t grant access to project',
                                   'error', info.context)
    else:
        rollbar.report_message(
            f'Error: Invalid role provided: {new_user_role}',
            f'error', info.context)

    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(new_user_email)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            (f'Security: Given grant access to {new_user_email} '
             f'in {project_name} project'))  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            (f'Security: Attempted to grant access to {new_user_email} '
             f'in {project_name} project'))  # pragma: no cover

    return GrantUserAccessPayloadType(
        success=success,
        granted_user=dict(
            project_name=project_name,
            email=new_user_email)
    )


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_remove_user_access(
        _, info,
        project_name: str, user_email: str) -> RemoveUserAccessPayloadType:
    """Resolve remove_user_access mutation."""
    success = False

    await sync_to_async(project_domain.remove_user_access)(
        project_name, user_email)
    success = \
        await sync_to_async(project_domain.remove_access)(
            user_email, project_name)
    removed_email = user_email if success else ''
    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(user_email)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Removed user: {user_email} from {project_name} '
            'project succesfully')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, f'Security: Attempted to remove user: {user_email} '
            f'from {project_name} project')  # pragma: no cover
    return RemoveUserAccessPayloadType(
        success=success,
        removed_email=removed_email
    )


@require_login
@enforce_group_level_auth_async
@require_project_access
async def _do_edit_user(_, info, **modified_user_data) -> EditUserPayloadType:
    """Resolve edit_user mutation."""
    project_name = modified_user_data['project_name'].lower()
    modified_role = modified_user_data['role']
    modified_email = modified_user_data['email']

    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    enforcer = authorization_utils.get_group_level_enforcer_async(user_email)
    if enforcer.enforce(user_email, project_name,
                        'backend_api_resolvers_user'
                        '__do_grant_user_access_internal_roles'):
        allowed_roles_to_grant = BASIC_ROLES + INTERNAL_ROLES
    else:
        allowed_roles_to_grant = BASIC_ROLES

    if modified_role in allowed_roles_to_grant:
        if await sync_to_async(user_domain.grant_group_level_role)(
                modified_email, project_name, modified_role):
            success = \
                await modify_user_information(
                    info.context, modified_user_data, project_name)
        else:
            await sync_to_async(rollbar.report_message)(
                'Error: Couldn\'t update user role', 'error', info.context)
    else:
        await sync_to_async(rollbar.report_message)(
            'Error: Invalid role provided: ' + modified_user_data['role'],
            'error', info.context)

    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(modified_email)
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            f'Security: Modified user data:{modified_email} '
            'in {project_name} project successfully')  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context,
            'Security: Attempted to modify user '
            f'data:{modified_email} in '
            f'{project_name} project')  # pragma: no cover

    return EditUserPayloadType(
        success=success,
        modified_user=dict(project_name=project_name,
                           email=modified_user_data['email'])
    )


@sync_to_async
def modify_user_information(context: object,
                            modified_user_data: Dict[str, str],
                            project_name: str) -> bool:
    """Modify user information."""
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    organization = modified_user_data['organization']
    user_domain.update(email, organization.lower(), 'company')
    successes = []

    if responsibility and len(responsibility) <= 50:
        result = project_domain.add_access(
            email, project_name, 'responsibility', responsibility)
        successes.append(result)
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to add responsibility to project \
                {project_name} bypassing validation')  # pragma: no cover
        successes.append(False)

    if phone and validate_phone_field(phone):
        result = user_domain.add_phone_to_user(email, phone)
        successes.append(result)
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to edit user phone bypassing \
                validation')  # pragma: no cover
        successes.append(False)

    return all(successes)


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
async def resolve_user_list_projects(_, info, user_email: str) -> List[str]:
    """Resolve user_list_projects query."""
    return await user_loader.resolve_user_list_projects(info, user_email)
