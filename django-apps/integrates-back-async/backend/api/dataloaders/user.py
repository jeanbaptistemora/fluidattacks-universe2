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
    has_responsibility, has_phone_number,
    has_access_to_project
)
from backend import util

from ariadne import convert_camel_case_to_snake


@sync_to_async
def _get_email(email, _=None):
    """Get email."""
    return dict(email=email.lower())


@sync_to_async
def _get_role(email, project_name):
    """Get role."""
    if project_name:
        role = user_domain.get_group_level_role(email, project_name)
    else:
        role = user_domain.get_user_level_role(email)

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


async def resolve(info, email, project_name, as_field=False):
    """Async resolve of fields."""
    email_dict: dict = await _get_email(email)
    role_dict: dict = await _get_role(email, project_name)
    email: str = email_dict['email']
    role: str = role_dict['role']

    if project_name and role:
        if not user_domain.get_data(email, 'email') or \
                not has_access_to_project(email, project_name):
            raise UserNotFound()

    result = dict()
    tasks = list()

    if not info.field_nodes[0].selection_set:
        requested_fields = ['listProjects']
    else:
        requested_fields = \
            util.get_requested_fields(
                'users', info.field_nodes[0].selection_set) \
            if as_field else info.field_nodes[0].selection_set.selections

    for requested_field in requested_fields:
        if isinstance(requested_field, str):
            requested_field = convert_camel_case_to_snake(requested_field)
        else:
            requested_field = \
                convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        tasks.append(
            asyncio.ensure_future(resolver_func(email, project_name))
        )
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result
