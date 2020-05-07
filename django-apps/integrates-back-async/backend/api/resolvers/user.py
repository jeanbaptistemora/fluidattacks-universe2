# pylint: disable=too-many-locals
from datetime import datetime
from typing import Dict, List, cast
import asyncio
import sys
import threading

from asgiref.sync import sync_to_async
from backend.api.resolvers import project as project_resolver
from backend.decorators import (
    require_login, require_project_access,
    enforce_group_level_auth_async,
    enforce_user_level_auth_async,
)
from backend.domain import project as project_domain, user as user_domain
from backend.exceptions import UserNotFound
from backend.mailer import send_mail_access_granted
from backend.typing import (
    User as UserType,
    AddUserPayload as AddUserPayloadType,
    GrantUserAccessPayload as GrantUserAccessPayloadType,
    RemoveUserAccessPayload as RemoveUserAccessPayloadType,
    EditUserPayload as EditUserPayloadType,
    Project as ProjectType,
)
from backend.services import (
    has_responsibility, has_phone_number,
    has_access_to_project
)
from backend.utils import authorization as authorization_utils
from backend.utils.validations import (
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)
from backend import util

import rollbar

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake

from __init__ import BASE_URL

# Constants
BASIC_ROLES = ['customer', 'customeradmin']
INTERNAL_ROLES = ['analyst']
ADMIN_ROLES = ['admin', 'closer', 'internal_manager', 'reviewer']


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
            f'{BASE_URL}/project/{group.lower()}/indicators'
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


@sync_to_async
def _get_email(_, email: str, **__) -> str:
    """Get email."""
    return email.lower()


@sync_to_async
def _get_role(_, email: str, project_name: str, **__) -> str:
    """Get role."""
    if project_name:
        role = user_domain.get_group_level_role(email, project_name)
    else:
        role = user_domain.get_user_level_role(email)

    return role


@sync_to_async
def _get_phone_number(_, email: str, **__) -> str:
    """Get phone number."""
    return has_phone_number(email)


@sync_to_async
def _get_responsibility(_, email: str, project_name: str, **__) -> str:
    """Get responsibility."""
    result = has_responsibility(
        project_name, email
    ) if project_name else ''
    return result


@sync_to_async
def _get_organization(_, email: str, **__) -> str:
    """Get organization."""
    org = cast(str, user_domain.get_data(email, 'company'))
    return org.title()


@sync_to_async
def _get_first_login(_, email: str, **__) -> str:
    """Get first login."""
    return cast(str, user_domain.get_data(email, 'date_joined'))


@sync_to_async
def _get_last_login(_, email: str, **__) -> str:
    """Get last_login."""
    last_login_response = cast(str, user_domain.get_data(email, 'last_login'))
    if last_login_response == '1111-1-1 11:11:11' or not last_login_response:
        last_login = [-1, -1]
    else:
        dates_difference = \
            datetime.now() - datetime.strptime(last_login_response,
                                               '%Y-%m-%d %H:%M:%S')
        diff_last_login = [dates_difference.days, dates_difference.seconds]
        last_login = diff_last_login
    return str(last_login)


async def _get_projects(info, email: str,
                        project_as_field: bool, **__) -> List[ProjectType]:
    """Get list projects."""
    list_projects = list()
    active = await sync_to_async(user_domain.get_projects)(email)
    inactive = \
        await sync_to_async(user_domain.get_projects)(email, active=False)
    user_projects = active + inactive
    list_projects = \
        [await project_resolver.resolve(
            info, project, as_field=project_as_field)
         for project in user_projects]
    return list_projects


async def resolve(info, email: str, project_name: str, as_field: bool = False,
                  selection_set: object = None) -> UserType:
    """Async resolve of fields."""
    email = await _get_email(info, email)
    role: dict = await _get_role(info, email, project_name=project_name)

    if project_name and role:
        if not user_domain.get_data(email, 'email') or \
                not has_access_to_project(email, project_name):
            raise UserNotFound()

    result = dict()
    requested_fields = \
        util.get_requested_fields('users', selection_set) \
        if as_field else info.field_nodes[0].selection_set.selections

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = \
            resolver_func(info, email,
                          project_name=project_name,
                          project_as_field=True)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
async def resolve_user(
        _, info, project_name: str, user_email: str) -> UserType:
    """Resolve user query."""
    return await resolve(info, user_email, project_name)


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
        util.cloudwatch_log(
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
                        '__do_grant_user_access_admin_roles'):
        allowed_roles_to_grant = BASIC_ROLES + INTERNAL_ROLES + ADMIN_ROLES
    elif enforcer.enforce(user_email, project_name,
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
        util.cloudwatch_log(
            info.context,
            (f'Security: Given grant access to {new_user_email} '
             f'in {project_name} project'))  # pragma: no cover
    else:
        util.cloudwatch_log(
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

    asyncio.create_task(
        sync_to_async(project_domain.remove_user_access)(
            project_name, user_email)
    )
    success = \
        await sync_to_async(project_domain.remove_access)(
            user_email, project_name)
    removed_email = user_email if success else ''
    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(user_email)
        util.cloudwatch_log(
            info.context,
            f'Security: Removed user: {user_email} from {project_name} '
            'project succesfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
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
                        '__do_grant_user_access_admin_roles'):
        allowed_roles_to_grant = BASIC_ROLES + INTERNAL_ROLES + ADMIN_ROLES
    elif enforcer.enforce(user_email, project_name,
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
        util.cloudwatch_log(
            info.context,
            f'Security: Modified user data:{modified_email} '
            'in {project_name} project successfully')  # pragma: no cover
    else:
        util.cloudwatch_log(
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
    successes = []

    if organization and validate_alphanumeric_field(organization):
        result = user_domain.update(email, organization.lower(), 'company')
        successes.append(result)
    else:
        successes.append(False)

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
async def resolve_user_list_projects(
        _, info, user_email: str) -> List[ProjectType]:
    """Resolve user_list_projects query."""
    email: str = await _get_email(info, user_email)

    return await _get_projects(info, email, project_as_field=False)
