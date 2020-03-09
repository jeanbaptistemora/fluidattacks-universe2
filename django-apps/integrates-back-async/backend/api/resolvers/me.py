# pylint: disable=import-error

from datetime import datetime, timedelta
import json

from backend.domain import user as user_domain
from backend.domain import project as project_domain
from backend.services import get_user_role, is_customeradmin
from backend.dal import user as user_dal
from backend import util

from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from graphql import GraphQLError
from jose import jwt
import rollbar

from ariadne import convert_kwargs_to_snake_case

from __init__ import FI_GOOGLE_OAUTH2_KEY_ANDROID, FI_GOOGLE_OAUTH2_KEY_IOS


def _get_role(jwt_content, project_name=None):
    """Get role."""
    role = get_user_role(jwt_content)
    if project_name and role == 'customer':
        email = jwt_content.get('user_email')
        role = 'customeradmin' if is_customeradmin(
            project_name, email) else 'customer'
    return role


def _get_projects(jwt_content):
    """Get projects."""
    projects = []
    user_email = jwt_content.get('user_email')
    for project in user_domain.get_projects(user_email):
        projects.append(
            dict(project_name=project,
                 description=project_domain.get_description(project))
        )
    return projects


def _get_access_token(jwt_content):
    """Get access token."""
    user_email = jwt_content.get('user_email')
    access_token = user_domain.get_data(user_email, 'access_token')
    access_token_dict = {
        'hasAccessToken': bool(access_token),
        'issuedAt': str(access_token.get('iat', '')) if bool(access_token) else ''
    }
    return json.dumps(access_token_dict)


def _get_authorized(jwt_content):
    """Get user authorization."""
    user_email = jwt_content.get('user_email')
    return user_domain.is_registered(user_email)


def _get_remember(jwt_content):
    """Get remember preference."""
    user_email = jwt_content.get('user_email')
    remember = user_domain.get_data(user_email, 'legal_remember')
    return remember if remember else False


@convert_kwargs_to_snake_case
def resolve_me(_, info):
    """Resolve Me query."""
    jwt_content = util.get_jwt_content(info.context)
    return dict(
        access_token=_get_access_token(jwt_content),
        authorized=_get_authorized(jwt_content),
        projects=_get_projects(jwt_content),
        remember=_get_remember(jwt_content),
        role=_get_role(jwt_content),
    )


@convert_kwargs_to_snake_case
def resolve_sign_in(_, info, auth_token, provider, push_token):
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
                    'user_role': user_domain.get_data(email, 'role'),
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

    return dict(authorized, session_jwt, success)
