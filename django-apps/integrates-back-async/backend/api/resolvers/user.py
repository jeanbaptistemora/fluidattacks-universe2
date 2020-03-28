# pylint: disable=import-error
# pylint: disable=too-many-locals

from datetime import datetime
from typing import Union, Dict, List as _List
import asyncio
import sys
import threading

from asgiref.sync import sync_to_async
from backend.decorators import (
    get_cached, require_login, require_project_access,
    enforce_group_level_auth_async,
    enforce_user_level_auth_async,
)
from backend.domain import project as project_domain, user as user_domain
from backend.exceptions import UserNotFound
from backend.mailer import send_mail_access_granted
from backend.services import (
    has_responsibility, has_phone_number, is_customeradmin,
    has_access_to_project
)
from backend.utils.validations import (
    validate_email_address, validate_alphanumeric_field, validate_phone_field
)

from backend import util

import rollbar

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


# I preffer being explicit in the arguments, easier to follow
# pylint: disable=too-many-arguments
def _create_new_user(
        context: Dict[str, Union[int, _List[str]]],
        email: str,
        organization: str,
        responsibility: str,
        role: str,
        phone_number: str,
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
            'Security: {email} Attempted to add responsibility to project \
                {project} without validation'.format(email=email,
                                                     project=group)
        )
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


@sync_to_async
def _get_email(email, _=None):
    """Get email."""
    return dict(email=email.lower())


@sync_to_async
def _get_role(email, project_name):
    """Get role."""
    user_role = user_domain.get_data(email, 'role')
    if project_name and is_customeradmin(project_name, email):
        role = 'customer_admin'
    elif user_role == 'customeradmin':
        role = 'customer'
    else:
        role = user_role
    return dict(role=role)


@sync_to_async
def _get_phone_number(email, _=None):
    """Get phone number."""
    result = has_phone_number(email)
    return dict(phone_number=result)


@sync_to_async
def _get_responsibility(email, project_name):
    """Get responsibility."""
    result = has_responsibility(
        project_name, email
    ) if project_name else ''
    return dict(responsibility=result)


@sync_to_async
def _get_organization(email, _=None):
    """Get organization."""
    org = user_domain.get_data(email, 'company')
    return dict(organization=org.title())


@sync_to_async
def _get_first_login(email, _=None):
    """Get first login."""
    result = user_domain.get_data(email, 'date_joined')
    return dict(first_login=result)


@sync_to_async
def _get_last_login(email, _=None):
    """Get last_login."""
    last_login = user_domain.get_data(email, 'last_login')
    if last_login == '1111-1-1 11:11:11' or not last_login:
        last_login = [-1, -1]
    else:
        dates_difference = \
            datetime.now() - datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
        diff_last_login = [dates_difference.days, dates_difference.seconds]
        last_login = diff_last_login
    return dict(last_login=str(last_login))


@sync_to_async
def _get_list_projects(email, project_name):
    """Get list projects."""
    list_projects = list()
    if not project_name:
        projs_active = \
            ['{proj}: {description} - Active'.format(
                proj=proj,
                description=project_domain.get_description(proj))
                for proj in user_domain.get_projects(email)]
        projs_suspended = \
            ['{proj}: {description} - Suspended'.format(
                proj=proj,
                description=project_domain.get_description(proj))
                for proj in user_domain.get_projects(
                    email, active=False)]
        list_projects = projs_active + projs_suspended
    return dict(list_projects=list_projects)


async def _resolve_fields(info, email, project_name):
    """Async resolve of fields."""
    email_dict: dict = await _get_email(email)
    role_dict: dict = await _get_role(email, project_name)
    email: str = email_dict['email']
    role: str = role_dict['role']

    if project_name and role:
        has_access = has_access_to_project(email, project_name)

        if not user_domain.get_data(email, 'email') or \
                not has_access:
            raise UserNotFound()

    result = dict()
    tasks = list()
    for requested_field in info.field_nodes[0].selection_set.selections:
        snake_field = convert_camel_case_to_snake(requested_field.name.value)
        if snake_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snake_field}'
        )
        future = asyncio.ensure_future(resolver_func(email, project_name))
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
@get_cached
def resolve_user(_, info, project_name, user_email):
    """Resolve user query."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        _resolve_fields(info, user_email, project_name)
    )
    loop.close()
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
def resolve_add_user(_, info, **parameters):
    """Resolve add_user mutation."""
    success = user_domain.create_without_project(parameters)
    if success:
        email = parameters.get('email', '').lower()
        util.cloudwatch_log(info.context, f'Security: Add user {email}')
        mail_to = [email]
        context = {'admin': email}
        email_send_thread = threading.Thread(
            name='Access granted email thread',
            target=send_mail_access_granted,
            args=(mail_to, context,)
        )
        email_send_thread.start()
    return dict(success=success, email=parameters.get('email', '').lower())


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_grant_user_access(_, info, **query_args):
    """Resolve grant_user_access mutation."""
    project_name = query_args.get('project_name')
    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    role = user_domain.get_group_level_role(user_email, project_name)

    new_user_role = query_args.get('role')
    new_user_email = query_args.get('email')

    roles_admin_can_grant = ('admin', 'analyst', 'customer', 'customeradmin')
    roles_customeradmin_can_grant = ('customer', 'customeradmin')

    if (role == 'admin' and new_user_role in roles_admin_can_grant) \
        or (is_customeradmin(project_name, user_email)
            and new_user_role in roles_customeradmin_can_grant):
        if _create_new_user(
                context=info.context,
                email=new_user_email,
                organization=query_args.get('organization'),
                responsibility=query_args.get('responsibility', '-'),
                role=query_args.get('role'),
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
        util.invalidate_cache(query_args.get('email'))
        util.cloudwatch_log(
            info.context, 'Security: Given grant access to {user} \
            in {project} project'.format(user=query_args.get('email'),
                                         project=project_name))
    else:
        util.cloudwatch_log(info.context, 'Security: Attempted to give grant \
access to {user} in {project} project'.format(user=query_args.get('email'),
                                              project=project_name))
    return dict(
        success=success,
        granted_user=dict(
            project_name=project_name,
            email=new_user_email)
    )


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_remove_user_access(
    _, info, project_name: str, user_email: str
) -> object:
    """Resolve remove_user_access mutation."""
    success = False

    project_domain.remove_user_access(project_name, user_email)
    success = project_domain.remove_access(user_email, project_name)
    removed_email = user_email if success else None
    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(user_email)
        util.cloudwatch_log(
            info.context,
            f'Security: Removed user: {user_email} from {project_name} \
            project succesfully')
    else:
        util.cloudwatch_log(
            info.context, f'Security: Attempted to remove user: {user_email}\
            from {project_name} project')
    return dict(success=success, removed_email=removed_email)


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_edit_user(_, info, **query_args):
    """Resolve edit_user mutation."""
    project_name = query_args.get('project_name')
    success = False
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    role = user_domain.get_group_level_role(user_email, project_name)

    modified_user_data = {
        'email': query_args.get('email'),
        'organization': query_args.get('organization'),
        'responsibility': query_args.get('responsibility'),
        'role': query_args.get('role'),
        'phone_number': query_args.get('phone_number')
    }
    if (role == 'admin'
            and modified_user_data['role'] in ['admin', 'analyst',
                                               'customer', 'customeradmin']) \
        or (is_customeradmin(project_name, user_data['user_email'])
            and modified_user_data['role'] in ['customer', 'customeradmin']):

        modified_user_email = modified_user_data['email']
        modified_user_role = modified_user_data['role']

        if user_domain.grant_group_level_role(
                modified_user_email, project_name, modified_user_role):
            modify_user_information(info.context, modified_user_data,
                                    project_name)
            success = True
        else:
            rollbar.report_message('Error: Couldn\'t update user role',
                                   'error', info.context)
    else:
        rollbar.report_message('Error: Invalid role provided: ' +
                               modified_user_data['role'], 'error',
                               info.context)
    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(query_args.get('email'))
        util.cloudwatch_log(
            info.context,
            f'Security: Modified user data:{query_args.get("email")} \
            in {project_name} project succesfully')
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to modify user \
            data:{query_args.get("email")} in {project_name} project')
    return dict(
        success=success,
        modified_user=dict(project_name=project_name,
                           email=modified_user_data['email']))


def modify_user_information(
        context: Dict[str, Union[int, _List[str]]],
        modified_user_data: Dict[str, str],
        project_name: str):
    """Modify user information."""
    role = modified_user_data['role']
    email = modified_user_data['email']
    responsibility = modified_user_data['responsibility']
    phone = modified_user_data['phone_number']
    organization = modified_user_data['organization']
    user_domain.update(email, organization.lower(), 'company')
    if responsibility and len(responsibility) <= 50:
        project_domain.add_access(
            email, project_name, 'responsibility', responsibility)
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to add responsibility to project \
                {project_name} bypassing validation')
    if phone and phone[1:].isdigit():
        user_domain.add_phone_to_user(email, phone)
    else:
        util.cloudwatch_log(
            context,
            f'Security: {email} Attempted to edit user phone bypassing \
                validation')
    if role == 'customeradmin':
        user_domain.grant_group_level_role(email, project_name, role)
    elif is_customeradmin(project_name, email):
        project_domain.remove_user_access(project_name, email)
