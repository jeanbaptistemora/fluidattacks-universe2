# pylint: disable=import-error

import json

from backend.domain import user as user_domain
from backend.domain import project as project_domain
from backend.services import get_user_role, is_customeradmin
from backend import util

from ariadne import convert_kwargs_to_snake_case


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
