# pylint: disable=import-error
# pylint: disable=too-many-locals

from datetime import datetime
from typing import List as _List
import threading

from backend.domain import project as project_domain, user as user_domain
from backend.exceptions import UserNotFound
from backend.mailer import send_mail_access_granted
from backend.services import (
    has_responsibility, has_phone_number, is_customeradmin,
    has_access_to_project
)
from backend import util

from ariadne import convert_kwargs_to_snake_case


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
