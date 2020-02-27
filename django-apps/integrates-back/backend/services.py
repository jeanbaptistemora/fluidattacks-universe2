""" FluidIntegrates services definition """

from typing import Any, Dict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from backend.domain import (
    event as event_domain, finding as finding_domain, user as user_domain
)

from backend import util
from backend.dal import project as project_dal


@csrf_exempt
@require_http_methods(["POST"])
def login(request: Any) -> Any:
    """ Authentication service defintion. """
    username = request.session['username']
    return util.response([], 'Bienvenido ' + username, False)


def is_registered(user: str) -> bool:
    """ Verify if the user is registered. """
    return user_domain.is_registered(user)


def has_access_to_project(user: str, project_name: str, rol: str) -> bool:
    """ Verify if the user has access to a project. """
    if rol == 'admin':
        return True
    return user_domain.get_project_access(user, project_name)


def has_access_to_finding(user: str, finding_id: str, role: str) -> bool:
    """ Verify if the user has access to a finding submission. """
    has_access = False
    # Skip this check for admin users since they don't have any assigned projects
    if role == 'admin':
        has_access = True
    else:
        finding = finding_domain.get_finding(finding_id)
        has_access = has_access_to_project(
            user, finding.get('projectName'), role)

    return has_access


def has_access_to_event(user: str, event_id: str, role: str) -> bool:
    """ Verify if the user has access to a event submission. """
    has_access = False
    # Skip this check for admin users since they don't have any assigned projects
    if role == 'admin':
        has_access = True
    else:
        finding = event_domain.get_event(event_id)
        has_access = has_access_to_project(
            user, finding.get('project_name'), role)  # type: ignore

    return has_access


def is_customeradmin(project: str, email: str) -> bool:
    """Verify if a user is a customeradmin."""
    project_data = project_dal.get(project)
    for data in project_data:
        if data.get('customeradmin') and email.lower() in data['customeradmin']:
            return True
    return False


def has_valid_access_token(email: str, context: Dict[Any, Any], jti: str) -> bool:
    """ Verify if has active access token and match. """
    access_token = user_domain.get_data(email, 'access_token')
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
            user_resp = data["responsibility"]
            break
        user_resp = "-"
    return user_resp


def has_phone_number(email: str) -> str:
    user_info = user_domain.get_data(email, 'phone')
    user_phone = user_info if user_info else '-'
    return user_phone


def get_user_role(user_data: Dict[Any, Any]) -> str:
    if user_data.get('jti'):
        role = user_domain.get_data(user_data['user_email'], 'role')
        if role == 'customeradmin':
            role = 'customer'
    else:
        role = user_data['user_role']
    return role


def project_exists(project_name: str) -> bool:
    return project_dal.exists(project_name)
