# pylint: disable=import-error

from datetime import datetime
import asyncio
import sys

from asgiref.sync import sync_to_async
from backend.domain import (
    project as project_domain,
    user as user_domain
)
from backend.exceptions import UserNotFound
from backend.services import (
    has_responsibility, has_phone_number, is_customeradmin,
    has_access_to_project
)

from ariadne import convert_camel_case_to_snake


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


async def resolve(info, email, project_name):
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
