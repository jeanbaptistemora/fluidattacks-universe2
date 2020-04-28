from datetime import datetime
import sys

from asgiref.sync import sync_to_async
from backend.api.resolvers import project as project_resolver
from backend.domain import user as user_domain
from backend.exceptions import UserNotFound
from backend.services import (
    has_responsibility, has_phone_number,
    has_access_to_project
)
from backend import util

from ariadne import convert_camel_case_to_snake


@sync_to_async
def _get_email(_, email, **__):
    """Get email."""
    return email.lower()


@sync_to_async
def _get_role(_, email, project_name, **__):
    """Get role."""
    if project_name:
        role = user_domain.get_group_level_role(email, project_name)
    else:
        role = user_domain.get_user_level_role(email)

    return role


@sync_to_async
def _get_phone_number(_, email, **__):
    """Get phone number."""
    return has_phone_number(email)


@sync_to_async
def _get_responsibility(_, email, project_name, **__):
    """Get responsibility."""
    result = has_responsibility(
        project_name, email
    ) if project_name else ''
    return result


@sync_to_async
def _get_organization(_, email, **__):
    """Get organization."""
    org = user_domain.get_data(email, 'company')
    return org.title()


@sync_to_async
def _get_first_login(_, email, **__):
    """Get first login."""
    return user_domain.get_data(email, 'date_joined')


@sync_to_async
def _get_last_login(_, email, **__):
    """Get last_login."""
    last_login = user_domain.get_data(email, 'last_login')
    if last_login == '1111-1-1 11:11:11' or not last_login:
        last_login = [-1, -1]
    else:
        dates_difference = \
            datetime.now() - datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
        diff_last_login = [dates_difference.days, dates_difference.seconds]
        last_login = diff_last_login
    return str(last_login)


async def _get_projects(info, email, project_as_field, **__):
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


async def resolve(info, email, project_name, as_field=False,
                  selection_set=None):
    """Async resolve of fields."""
    email: dict = await _get_email(info, email)
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


async def resolve_user_list_projects(info, email):
    """Async resolve of fields."""
    email: dict = await _get_email(info, email)

    requested_fields = info.field_nodes[0].selection_set.selections

    requested_field = requested_fields[0]
    params = {
        'email': email,
        'project_name': None,
        'project_as_field': False
    }
    field_params = util.get_field_parameters(requested_field)
    if field_params:
        params.update(field_params)
    requested_field = \
        convert_camel_case_to_snake(requested_field.name.value)
    return await _get_projects(info, **params)
