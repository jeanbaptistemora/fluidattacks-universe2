""" FluidIntegrates services definition """

from typing import Dict, cast
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from backend.domain import (
    event as event_domain, finding as finding_domain, user as user_domain
)

from backend import authz, util
from backend.dal import project as project_dal


@csrf_exempt
@require_http_methods(["POST"])
def login(request) -> JsonResponse:
    """ Authentication service defintion. """
    username = request.session['username']
    return util.response([], 'Bienvenido ' + username, False)


def is_registered(user: str) -> bool:
    """ Verify if the user is registered. """
    return user_domain.is_registered(user)


def has_access_to_project(email: str, group: str) -> bool:
    """ Verify if the user has access to a project. """
    return bool(authz.get_group_level_role(email, group))


def has_access_to_finding(email: str, finding_id: str) -> bool:
    """ Verify if the user has access to a finding submission. """
    finding = finding_domain.get_finding(finding_id)
    group = cast(str, finding.get('projectName', ''))
    return has_access_to_project(email, group)


def has_access_to_event(email: str, event_id: str) -> bool:
    """ Verify if the user has access to a event submission. """
    event = event_domain.get_event(event_id)
    group = cast(str, event.get('project_name', ''))
    return has_access_to_project(email, group)


def has_valid_access_token(email: str, context: Dict[str, str], jti: str) -> bool:
    """ Verify if has active access token and match. """
    access_token = cast(Dict[str, str], user_domain.get_data(email, 'access_token'))
    resp = False
    if context and access_token:
        resp = util.verificate_hash_token(access_token, jti)
    else:
        # authorization header not present or user without access_token
        pass
    return resp


def has_responsibility(project: str, email: str) -> str:
    """Verify if a user has responsibility."""
    project_data = project_dal.get_user_access(email, project)
    user_resp = "-"
    for data in project_data:
        if 'responsibility' in data:
            user_resp = cast(str, data["responsibility"])
            break
        user_resp = "-"
    return user_resp


def has_phone_number(email: str) -> str:
    user_info = str(user_domain.get_data(email, 'phone'))
    user_phone = user_info if user_info else '-'
    return user_phone


def project_exists(project_name: str) -> bool:
    return project_dal.exists(project_name)
