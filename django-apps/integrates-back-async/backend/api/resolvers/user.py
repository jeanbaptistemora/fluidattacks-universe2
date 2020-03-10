# pylint: disable=import-error
# pylint: disable=too-many-locals

from datetime import datetime
from typing import Union, Dict, List as _List
import threading

from backend.domain import project as project_domain, user as user_domain
from backend.exceptions import UserNotFound
from backend.mailer import send_mail_access_granted
from backend.services import (
    get_user_role, has_responsibility, has_phone_number, is_customeradmin,
    has_access_to_project
)
from backend.utils.user import (
    validate_email_address, validate_field, validate_phone_field
)

from backend import util

import rollbar

from ariadne import convert_kwargs_to_snake_case


def _create_new_user(
        context: Dict[str, Union[int, _List[str]]],
        new_user_data: Dict[str, str],
        project_name: str) -> bool:
    analizable_list = list(new_user_data.values())[1:-1]
    if (
        all(validate_field(field) for field in analizable_list) and
        validate_phone_field(new_user_data['phone_number']) and
        validate_email_address(new_user_data['email'])
    ):
        email = new_user_data['email']
        organization = new_user_data['organization']
        responsibility = new_user_data['responsibility']
        role = new_user_data['role']
        phone_number = new_user_data['phone_number']
    else:
        return False

    success = False

    if not user_domain.get_data(email, 'email'):
        user_domain.create(
            email.lower(), {'company': organization.lower(),
                            'phone': phone_number})
    if not user_domain.is_registered(email):
        user_domain.register(email)
        user_domain.assign_role(email, role)
        user_domain.update(email, organization.lower(), 'company')
    elif user_domain.is_registered(email):
        user_domain.assign_role(email, role)
    if project_name and responsibility and len(responsibility) <= 50:
        project_domain.add_access(email, project_name, 'responsibility', responsibility)
    else:
        util.cloudwatch_log(
            context,
            'Security: {email} Attempted to add responsibility to project \
                {project} without validation'.format(email=email,
                                                     project=project_name)
        )
    if phone_number and phone_number[1:].isdigit():
        user_domain.add_phone_to_user(email, phone_number)
    if project_name and role == 'customeradmin':
        project_domain.add_user(project_name.lower(), email.lower(), role)
    if project_name and user_domain.update_project_access(email, project_name, True):
        description = project_domain.get_description(project_name.lower())
        project_url = \
            'https://fluidattacks.com/integrates/dashboard#!/project/' \
            + project_name.lower() + '/indicators'
        mail_to = [email]
        context = {
            'admin': email,
            'project': project_name,
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
def resolve_user(*_, project_name, user_email):
    """Resolve user query."""
    email: str = user_email
    role: str = ''
    responsability: str = ''
    phone_number: str = ''
    organization: str = ''
    first_login: str = '-'
    last_login: _List[int] = [-1, -1]
    list_projects: _List[int] = []
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

    last_login = user_domain.get_data(user_email, 'last_login')

    if last_login == '1111-1-1 11:11:11' or not last_login:
        last_login = [-1, -1]
    else:
        dates_difference = \
            datetime.now() - datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
        diff_last_login = [dates_difference.days, dates_difference.seconds]
        last_login = diff_last_login

    first_login = user_domain.get_data(user_email, 'date_joined')
    organization = user_domain.get_data(user_email, 'company')
    organization = organization.title()
    responsability = has_responsibility(
        project_name, user_email) if project_name else ''
    phone_number = has_phone_number(user_email)
    user_role = user_domain.get_data(user_email, 'role')

    if project_name and is_customeradmin(project_name, user_email):
        role = 'customer_admin'
    elif user_role == 'customeradmin':
        role = 'customer'
    else:
        role = user_role

    if project_name and role:
        if role == 'admin':
            has_access = has_access_to_project(
                user_email, project_name, role)
        else:
            has_access = user_domain.get_project_access(
                user_email, project_name)

        if not user_domain.get_data(user_email, 'email') or \
                not has_access:
            raise UserNotFound()
    return dict(
        email=email.lower(),
        role=role,
        responsability=responsability,
        phone_number=phone_number,
        organization=organization,
        first_login=first_login,
        last_login=last_login,
        list_projects=list_projects
    )


@convert_kwargs_to_snake_case
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
def resolve_grant_user_access(_, info, **query_args):
    """Resolve grant_user_access mutation."""
    project_name = query_args.get('project_name')
    success = False
    user_data = util.get_jwt_content(info.context)
    role = get_user_role(user_data)
    new_user_data = {
        'email': query_args.get('email'),
        'organization': query_args.get('organization'),
        'responsibility': query_args.get('responsibility', '-'),
        'role': query_args.get('role'),
        'phone_number': query_args.get('phone_number', '')
    }

    if (role == 'admin'
            and new_user_data['role'] in ['admin', 'analyst', 'customer', 'customeradmin']) \
        or (is_customeradmin(project_name, user_data['user_email'])
            and new_user_data['role'] in ['customer', 'customeradmin']):
        if _create_new_user(info.context, new_user_data, project_name):
            success = True
        else:
            rollbar.report_message('Error: Couldn\'t grant access to project',
                                   'error', info.context)
    else:
        rollbar.report_message('Error: Invalid role provided: ' +
                               new_user_data['role'], 'error', info.context)
    if success:
        util.invalidate_cache(project_name)
        util.invalidate_cache(query_args.get('email'))
        util.cloudwatch_log(info.context, 'Security: Given grant access to {user} \
            in {project} project'.format(user=query_args.get('email'), project=project_name))
    else:
        util.cloudwatch_log(info.context, 'Security: Attempted to give grant \
            access to {user} in {project} project'.format(user=query_args.get('email'),
                                                          project=project_name))
    return dict(
        success=success,
        granted_user=dict(
            project_name=project_name,
            email=new_user_data['email'])
    )
