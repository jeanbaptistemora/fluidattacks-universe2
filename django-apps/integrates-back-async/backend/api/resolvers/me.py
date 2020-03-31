# pylint: disable=import-error

from datetime import datetime, timedelta
import asyncio
import json
import sys

from collections import defaultdict
from typing import Any, Dict, List, Union
from asgiref.sync import sync_to_async
from backend.decorators import require_login
from backend.domain import user as user_domain
from backend.domain import project as project_domain
from backend.exceptions import InvalidExpirationTime
from backend.dal import user as user_dal
from backend.typing import User as UserType
from backend.services import is_customeradmin
from backend import util

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from graphql import GraphQLError
from jose import jwt
import rollbar

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake

from __init__ import FI_GOOGLE_OAUTH2_KEY_ANDROID, FI_GOOGLE_OAUTH2_KEY_IOS


@sync_to_async
def _get_role(
    jwt_content: Dict[str, str], project_name: str = None
) -> Dict[str, str]:
    """Get role."""
    user_email = jwt_content['user_email']

    if project_name:
        role = user_domain.get_group_level_role(user_email, project_name)
    else:
        role = user_domain.get_user_level_role(user_email)

    if project_name and role == 'customer':
        email = jwt_content.get('user_email', '')
        role = 'customeradmin' if is_customeradmin(
            project_name, email) else 'customer'
    return dict(role=role)


@sync_to_async
def _get_projects(
        jwt_content: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
    """Get projects."""
    projects = []
    user_email = jwt_content.get('user_email', '')
    for project in user_domain.get_projects(user_email):
        description = project_domain.get_description(project)
        projects.append(
            dict(name=project, description=description)
        )
    return dict(projects=projects)


@sync_to_async
def _get_access_token(jwt_content: Dict[str, str]) -> Dict[str, str]:
    """Get access token."""
    user_email = jwt_content.get('user_email', '')
    access_token = user_domain.get_data(user_email, 'access_token')
    access_token_dict = {
        'hasAccessToken': bool(access_token),
        'issuedAt': str(access_token.get('iat', ''))
        if isinstance(access_token, dict) else ''
    }
    return dict(access_token=json.dumps(access_token_dict))


@sync_to_async
def _get_authorized(jwt_content: Dict[str, str]) -> Dict[str, bool]:
    """Get user authorization."""
    user_email = jwt_content.get('user_email', '')
    result = user_domain.is_registered(user_email)
    return dict(authorized=result)


@sync_to_async
def _get_remember(
        jwt_content: Dict[str, str]) -> Dict[str, Union[bool, str, UserType]]:
    """Get remember preference."""
    user_email = jwt_content.get('user_email', '')
    remember = user_domain.get_data(user_email, 'legal_remember')
    result = remember if remember else False
    return dict(remember=result)


@sync_to_async
def _get_tags(
        jwt_content: Dict[str, str]) -> Dict[str, List]:
    """Get tags."""
    user_email = jwt_content.get('user_email', '')
    projects = user_domain.get_projects(user_email)
    tags_dict: Dict[str, List] = defaultdict(list)
    for project in projects:
        project_tag = project_domain.get_attributes(
            project, ['tag']).get('tag', [])
        for tag in project_tag:
            tags_dict[tag].append(dict(name=project))
    tags = []
    for tag, projects in tags_dict.items():
        tags.append(dict(name=tag, projects=projects))
    return dict(tags=tags)


async def _resolve_fields(info) -> Dict[int, Any]:
    """Async resolve fields."""
    result: Dict[int, Any] = dict()
    tasks = list()
    jwt_content = util.get_jwt_content(info.context)
    params = {
        'jwt_content': jwt_content
    }
    for requested_field in info.field_nodes[0].selection_set.selections:
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        tasks.append(
            asyncio.ensure_future(resolver_func(**params))
        )
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
def resolve_me(_, info) -> Dict[int, Any]:
    """Resolve Me query."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        _resolve_fields(info)
    )
    loop.close()
    return result


@convert_kwargs_to_snake_case
def resolve_sign_in(_, info, auth_token: str, provider: str,
                    push_token: str) -> Dict[str, Union[str, bool]]:
    """Resolve sign_in mutation."""
    authorized = False
    session_jwt = ''
    success = False

    if provider == 'google':
        try:
            user_info = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if user_info['iss'] not in ['accounts.google.com',
                                        'https://accounts.google.com']:
                rollbar.report_message(
                    'Error: Invalid oauth2 issuer',
                    'error', info.context, user_info['iss'])
                raise GraphQLError('INVALID_AUTH_TOKEN')
            if user_info['aud'] not in [FI_GOOGLE_OAUTH2_KEY_ANDROID,
                                        FI_GOOGLE_OAUTH2_KEY_IOS]:
                rollbar.report_message(
                    'Error: Invalid oauth2 audience',
                    'error', info.context, user_info['aud'])
                raise GraphQLError('INVALID_AUTH_TOKEN')
            email = user_info['email']
            authorized = user_domain.is_registered(email)
            if push_token:
                user_dal.update(email, {'devices_to_notify': set(push_token)})
            session_jwt = jwt.encode(
                {
                    'user_email': email,
                    'company': user_domain.get_data(email, 'company'),
                    'first_name': user_info['given_name'],
                    'last_name': user_info['family_name'],
                    'exp': datetime.utcnow() +
                    timedelta(seconds=settings.SESSION_COOKIE_AGE)
                },
                algorithm='HS512',
                key=settings.JWT_SECRET,
            )
            success = True
        except ValueError:
            util.cloudwatch_log(
                info.context,
                'Security: Sign in attempt using invalid Google token')
            raise GraphQLError('INVALID_AUTH_TOKEN')
    else:
        rollbar.report_message(
            'Error: Unknown auth provider' + provider, 'error')
        raise GraphQLError('UNKNOWN_AUTH_PROVIDER')

    return dict(
        authorized=authorized,
        session_jwt=session_jwt,
        success=success
    )


@convert_kwargs_to_snake_case
@require_login
def resolve_update_access_token(
        _, info, expiration_time: int) -> Dict[str, Union[str, bool]]:
    """Resolve update_access_token mutation."""
    user_info = util.get_jwt_content(info.context)
    email = user_info['user_email']
    token_data = util.calculate_hash_token()
    session_jwt = ''
    success = False

    if util.is_valid_expiration_time(expiration_time):
        session_jwt = jwt.encode(
            {
                'user_email': email,
                'company': user_domain.get_data(
                    email, 'company'),
                'first_name': user_info['first_name'],
                'last_name': user_info['last_name'],
                'jti': token_data['jti'],
                'iat': datetime.utcnow().timestamp(),
                'exp': expiration_time
            },
            algorithm='HS512',
            key=settings.JWT_SECRET_API
        )

        success = user_domain.update_access_token(email, token_data)
        if success:
            util.cloudwatch_log(
                info.context, '{email} update access token'.format(
                    email=user_info['user_email']))
        else:
            util.cloudwatch_log(
                info.context, '{email} attempted to update access token'
                .format(email=user_info['user_email']))
    else:
        util.cloudwatch_log(
            info.context, '{email} attempted to use expiration time \
            greater than six months or minor than current time'
            .format(email=user_info['user_email']))
        raise InvalidExpirationTime()

    return dict(success=success, session_jwt=session_jwt)


@convert_kwargs_to_snake_case
@require_login
def resolve_invalidate_access_token(_, info):
    """Resolve invalidate_access_token mutation."""
    user_info = util.get_jwt_content(info.context)

    success = user_domain.remove_access_token(user_info['user_email'])
    if success:
        util.cloudwatch_log(
            info.context, '{email} invalidate access token'.format(
                email=user_info['user_email']))
    else:
        util.cloudwatch_log(
            info.context, '{email} attempted to invalidate access token'
            .format(email=user_info['user_email']))
    return dict(success=success)


@convert_kwargs_to_snake_case
def resolve_accept_legal(_, info, remember: bool = False) -> Dict[str, bool]:
    """Resolve accept_legal mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    is_registered = user_domain.is_registered(user_email)

    if is_registered:
        user_domain.update_legal_remember(user_email, remember)
        success = True
    else:
        success = False
    return dict(success=success)
