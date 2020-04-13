# pylint: disable=import-error

from datetime import datetime, timedelta
import asyncio
import json
import sys

from collections import defaultdict
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from asgiref.sync import sync_to_async
from backend.decorators import require_login, enforce_user_level_auth_async
from backend.domain import user as user_domain
from backend.domain import project as project_domain
from backend.exceptions import InvalidExpirationTime
from backend.dal import user as user_dal
from backend.typing import User as UserType
from backend.utils import authorization as authorization_utils
from backend import util

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from graphql import GraphQLError
from jose import jwt
import rollbar

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake

from __init__ import FI_GOOGLE_OAUTH2_KEY_ANDROID, FI_GOOGLE_OAUTH2_KEY_IOS


async def _get_role(
    _, user_email: str, project_name: str = None
) -> Dict[str, str]:
    """Get role."""
    if project_name:
        role = await \
            sync_to_async(user_domain.get_group_level_role)(
                user_email, project_name)
    else:
        role = await \
            sync_to_async(user_domain.get_user_level_role)(user_email)
    return dict(role=role)


async def _get_projects(_, user_email: str) -> Dict[str, List[Dict[str, str]]]:
    """Get projects."""
    projects = []
    for project in await sync_to_async(user_domain.get_projects)(user_email):
        description = await \
            sync_to_async(project_domain.get_description)(project)
        projects.append(
            dict(name=project, description=description)
        )
    return dict(projects=projects)


async def _get_access_token(_, user_email: str) -> Dict[str, str]:
    """Get access token."""
    access_token = await sync_to_async(user_domain.get_data)(
        user_email, 'access_token')
    access_token_dict = {
        'hasAccessToken': bool(access_token),
        'issuedAt': str(access_token.get('iat', ''))
        if isinstance(access_token, dict) else ''
    }
    return dict(access_token=json.dumps(access_token_dict))


async def _get_authorized(_, user_email: str) -> Dict[str, bool]:
    """Get user authorization."""
    result = await sync_to_async(user_domain.is_registered)(user_email)
    return dict(authorized=result)


async def _get_remember(
        _, user_email: str) -> Dict[str, Union[bool, str, UserType]]:
    """Get remember preference."""
    remember = await \
        sync_to_async(user_domain.get_data)(user_email, 'legal_remember')
    result = remember or False
    return dict(remember=result)


async def _get_permissions(
    _, user_email: str, project_name: Optional[str] = None
) -> Dict[str, Tuple[str, ...]]:
    """Get the actions the user is allowed to perform."""
    subject = user_email
    object_ = project_name if project_name else 'self'
    enforcer = \
        authorization_utils.get_group_level_enforcer_async(subject) \
        if project_name else \
        authorization_utils.get_user_level_enforcer_async(subject)
    permissions = tuple([
        action for action in authorization_utils.list_actions()
        if enforcer.enforce(subject, object_, action)])
    return dict(permissions=permissions)


@enforce_user_level_auth_async
async def _get_tags(
        _, user_email: str) -> Dict[str, List[Dict[str, Sequence[str]]]]:
    """Get tags."""
    projects = await \
        sync_to_async(user_domain.get_projects)(user_email)
    tags_dict: Dict[str, List] = defaultdict(list)
    for project in projects:
        project_tag = await sync_to_async(project_domain.get_attributes)(
            project, ['tag'])
        project_tag = project_tag.get('tag', [])
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

    for requested_field in info.field_nodes[0].selection_set.selections:
        if util.is_skippable(info, requested_field):
            continue
        jwt_content = util.get_jwt_content(info.context)
        params = {
            'user_email': jwt_content.get('user_email')
        }
        field_params = util.get_field_parameters(
            requested_field, info.variable_values)
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
            asyncio.ensure_future(resolver_func(info, **params))
        )
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
def resolve_me(_, info) -> Dict[int, Any]:
    """Resolve Me query."""
    return util.run_async(_resolve_fields, info)


@convert_kwargs_to_snake_case
def resolve_me_mutation(obj, info, **parameters):
    """Wrap me mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return util.run_async(resolver_func, obj, info, **parameters)


async def _do_sign_in(_, info, auth_token: str, provider: str,
                      push_token: str) -> Dict[str, Union[str, bool]]:
    """Resolve sign_in mutation."""
    authorized = False
    session_jwt = ''
    success = False

    if provider == 'google':
        try:
            user_info = await sync_to_async(id_token.verify_oauth2_token)(
                auth_token, requests.Request())

            if user_info['iss'] not in ['accounts.google.com',
                                        'https://accounts.google.com']:
                await sync_to_async(rollbar.report_message)(
                    'Error: Invalid oauth2 issuer',
                    'error', info.context, user_info['iss'])
                raise GraphQLError('INVALID_AUTH_TOKEN')
            if user_info['aud'] not in [FI_GOOGLE_OAUTH2_KEY_ANDROID,
                                        FI_GOOGLE_OAUTH2_KEY_IOS]:
                await sync_to_async(rollbar.report_message)(
                    'Error: Invalid oauth2 audience',
                    'error', info.context, user_info['aud'])
                raise GraphQLError('INVALID_AUTH_TOKEN')
            email = user_info['email']
            authorized = await sync_to_async(user_domain.is_registered)(email)
            if push_token:
                await \
                    sync_to_async(user_dal.update)(
                        email, {'devices_to_notify': set(push_token)}
                    )
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
            await sync_to_async(util.cloudwatch_log)(
                info.context,
                'Security: Sign in attempt '
                'using invalid Google token')  # pragma: no cover
            raise GraphQLError('INVALID_AUTH_TOKEN')
    else:
        await sync_to_async(rollbar.report_message)(
            'Error: Unknown auth provider' + provider, 'error')
        raise GraphQLError('UNKNOWN_AUTH_PROVIDER')

    return dict(
        authorized=authorized,
        session_jwt=session_jwt,
        success=success
    )


@require_login
async def _do_update_access_token(
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

        success = await \
            sync_to_async(user_domain.update_access_token)(email, token_data)
        if success:
            await sync_to_async(util.cloudwatch_log)(
                info.context, '{email} update access token'.format(
                    email=user_info['user_email']))  # pragma: no cover
        else:
            await sync_to_async(util.cloudwatch_log)(
                info.context, '{email} attempted to update access token'
                .format(email=user_info['user_email']))  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, '{email} attempted to use expiration time \
            greater than six months or minor than current time'
            .format(email=user_info['user_email']))  # pragma: no cover
        raise InvalidExpirationTime()

    return dict(success=success, session_jwt=session_jwt)


@require_login
async def _do_invalidate_access_token(_, info):
    """Resolve invalidate_access_token mutation."""
    user_info = util.get_jwt_content(info.context)

    success = await \
        sync_to_async(user_domain.remove_access_token)(user_info['user_email'])
    if success:
        await sync_to_async(util.cloudwatch_log)(
            info.context, '{email} invalidate access token'.format(
                email=user_info['user_email']))  # pragma: no cover
    else:
        await sync_to_async(util.cloudwatch_log)(
            info.context, '{email} attempted to invalidate access token'
            .format(email=user_info['user_email']))  # pragma: no cover
    return dict(success=success)


async def _do_accept_legal(_, info, remember: bool = False) -> Dict[str, bool]:
    """Resolve accept_legal mutation."""
    user_email = util.get_jwt_content(info.context)['user_email']
    is_registered = await sync_to_async(user_domain.is_registered)(user_email)

    if is_registered:
        await \
            sync_to_async(user_domain.update_legal_remember)(
                user_email, remember
            )
        success = True
    else:
        success = False
    return dict(success=success)
