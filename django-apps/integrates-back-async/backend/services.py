""" FluidIntegrates services definition """

from typing import Dict, cast
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from backend.domain import (
    event as event_domain,
    finding as finding_domain,
    user as user_domain
)

from backend import authz, util
from backend.dal import project as project_dal


@csrf_exempt  # type: ignore
@require_http_methods(["POST"])  # type: ignore
def login(request: HttpRequest) -> JsonResponse:
    """ Authentication service defintion. """
    username = request.session['username']
    return util.response([], 'Bienvenido ' + username, False)


async def has_access_to_project(email: str, group: str) -> bool:
    """ Verify if the user has access to a project. """
    return bool(await authz.get_group_level_role(email, group.lower()))


async def has_access_to_finding(email: str, finding_id: str) -> bool:
    """ Verify if the user has access to a finding submission. """
    finding = await finding_domain.get_finding(finding_id)
    group = cast(str, finding.get('projectName', ''))
    return await has_access_to_project(email, group)


async def has_access_to_event(email: str, event_id: str) -> bool:
    """ Verify if the user has access to a event submission. """
    event = await event_domain.get_event(event_id)
    group = cast(str, event.get('project_name', ''))
    return await has_access_to_project(email, group)


async def has_valid_access_token(
        email: str, context: Dict[str, str], jti: str) -> bool:
    """ Verify if has active access token and match. """
    access_token = cast(
        Dict[str, str],
        await user_domain.get_data(email, 'access_token')
    )
    resp = False
    if context and access_token:
        resp = util.verificate_hash_token(access_token, jti)
    else:
        # authorization header not present or user without access_token
        pass
    return resp


async def has_responsibility(project: str, email: str) -> str:
    """Verify if a user has responsibility."""
    project_data = await project_dal.get_user_access(email, project)
    user_resp = "-"
    for data in project_data:
        if 'responsibility' in data:
            user_resp = cast(str, data["responsibility"])
            break
        user_resp = "-"
    return user_resp


async def has_phone_number(email: str) -> str:
    user_info = str(await user_domain.get_data(email, 'phone'))
    user_phone = user_info if user_info else '-'
    return user_phone
