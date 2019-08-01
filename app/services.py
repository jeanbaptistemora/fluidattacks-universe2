""" FluidIntegrates services definition """

import rollbar
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# pylint: disable=E0402
from . import util
# pylint: disable=E0402
from .dao import integrates_dao
from .dao.helpers.formstack import FormstackAPI
from .dto.finding import FindingDTO
from .dto.eventuality import EventDTO


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """ Authentication service defintion. """
    username = request.session['username']
    return util.response([], 'Bienvenido ' + username, False)


def is_registered(user):
    """ Verify if the user is registered. """
    return integrates_dao.is_registered_dao(user)


def has_access_to_project(user, project_name, rol):
    """ Verify if the user has access to a project. """
    if rol == 'admin':
        return True
    return integrates_dao.has_access_to_project_dao(user, project_name)


def has_access_to_finding(user, findingid, role):
    """ Verify if the user has access to a finding submission. """
    has_access = False
    # Skip this check for admin users since they don't have any assigned projects
    if role == 'admin':
        has_access = True
    else:
        project = integrates_dao.get_finding_project(findingid)

        if project:
            has_access = has_access_to_project(user, project, role)
        else:
            api = FormstackAPI()
            fin_dto = FindingDTO()
            finding_data = fin_dto.parse_project(api.get_submission(findingid), findingid)
            project = finding_data['projectName'] if 'projectName' in finding_data else None

            if project:
                has_access = has_access_to_project(user, project, role)
            else:
                rollbar.report_message(
                    'Error: An error ocurred getting finding project', 'error')
    return has_access


def has_access_to_event(user, event_id, role):
    """ Verify if the user has access to a event submission. """
    has_access = False
    # Skip this check for admin users since they don't have any assigned projects
    if role == 'admin':
        has_access = True
    else:
        project = integrates_dao.get_event_project(event_id)

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
    project_data = integrates_dao.get_project_dynamo(project)
    for data in project_data:
        if data.get('customeradmin') and email.lower() in data['customeradmin']:
            return True
    return False


def has_responsibility(project, email):
    """Verify if a user has responsibility."""
    project_data = integrates_dao.get_project_access_dynamo(email, project)
    user_resp = "-"
    for data in project_data:
        if 'responsibility' in data:
            user_resp = data["responsibility"]
            break
        else:
            user_resp = "-"
    return user_resp


def has_phone_number(email):
    user_info = integrates_dao.get_user_dynamo(email)
    for user in user_info:
        if 'phone' in user:
            return user["phone"]
    user_phone = "-"
    return user_phone
