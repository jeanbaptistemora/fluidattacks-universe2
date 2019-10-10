""" FluidIntegrates services definition """

import rollbar
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from app import util
from app.dal import integrates_dal
from app.dal.helpers.formstack import FormstackAPI
from app.domain import finding as finding_domain, user as user_domain
from app.dto.eventuality import EventDTO


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """ Authentication service defintion. """
    username = request.session['username']
    return util.response([], 'Bienvenido ' + username, False)


def is_registered(user):
    """ Verify if the user is registered. """
    return user_domain.is_registered(user)


def has_access_to_project(user, project_name, rol):
    """ Verify if the user has access to a project. """
    if rol == 'admin':
        return True
    return integrates_dal.has_access_to_project(user, project_name)


def has_access_to_finding(user, finding_id, role):
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


def has_access_to_event(user, event_id, role):
    """ Verify if the user has access to a event submission. """
    has_access = False
    # Skip this check for admin users since they don't have any assigned projects
    if role == 'admin':
        has_access = True
    else:
        project = integrates_dal.get_event_project(event_id)

        if project:
            has_access = has_access_to_project(user, project, role)
        else:
            api = FormstackAPI()
            evt_dto = EventDTO()
            event_data = evt_dto.parse(event_id, api.get_submission(event_id))
            project = event_data.get('projectName', '')
            if project:
                has_access = has_access_to_project(user, project, role)
            else:
                rollbar.report_message(
                    'Error: Event {event_id} does not have project'.format(
                        event_id=event_id),
                    'error')
    return has_access


def is_customeradmin(project, email):
    """Verify if a user is a customeradmin."""
    project_data = integrates_dal.get_project_dynamo(project)
    for data in project_data:
        if data.get('customeradmin') and email.lower() in data['customeradmin']:
            return True
    return False


def has_valid_access_token(email, context, jti):
    """ Verify if has active access token and match. """
    access_token = user_domain.get_data(email, 'access_token')
    resp = False
    if context and access_token:
        resp = util.verificate_hash_token(access_token, jti)
    else:
        # authorization header not present or user without access_token
        pass
    return resp


def has_responsibility(project, email):
    """Verify if a user has responsibility."""
    project_data = integrates_dal.get_project_access_dynamo(email, project)
    user_resp = "-"
    for data in project_data:
        if 'responsibility' in data:
            user_resp = data["responsibility"]
            break
        else:
            user_resp = "-"
    return user_resp


def has_phone_number(email):
    user_info = user_domain.get_data(email, 'phone')
    user_phone = user_info if user_info else '-'
    return user_phone


def get_user_role(user_data):
    if user_data.get('jti'):
        role = user_domain.get_data(user_data['user_email'], 'role')
    else:
        role = user_data['user_role']
    return role
