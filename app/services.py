""" FluidIntegrates services definition """

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# pylint: disable=E0402
from . import util
# pylint: disable=E0402
from .dao import integrates_dao
from .api.formstack import FormstackAPI
from .dto.finding import FindingDTO
from .dto.eventuality import EventDTO

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """ Authentication service defintion. """
    username = request.session['username']
    return util.response([], 'Bienvenido ' + username, False)


def get_company(user):
    """ Gets the company to which the user belongs. """
    return integrates_dao.get_organization_dao(user)


def get_role(user):
    """ Gets the role of a user. """
    return integrates_dao.get_role_dao(user)


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
    hasAccess = False
    # Skip this check for admin users since they don't have any assigned projects
    if role == 'admin':
        hasAccess = True
    else:
        project = integrates_dao.get_finding_project(findingid)

        if project:
            hasAccess = has_access_to_project(user, project, role)
        else:
            api = FormstackAPI()
            fin_dto = FindingDTO()
            evt_dto = EventDTO()
            finding_data = fin_dto.parse_project(api.get_submission(findingid), findingid)
            project = finding_data['projectName'] if 'projectName' in finding_data else None

            if project:
                hasAccess = has_access_to_project(user, project, role)
            else:
                project = evt_dto.parse(findingid, api.get_submission(findingid))['projectName']
                hasAccess = has_access_to_project(user, project, role)
    return hasAccess

def is_customeradmin(project, email):
    """Verify if a user is a customeradmin."""
    project_data = integrates_dao.get_project_dynamo(project)
    for data in project_data:
        if data.get('customeradmin'):
            if email.lower() in data["customeradmin"]:
                return True
    return False

def has_responsibility(project, email):
    """Verify if a user has responsability."""
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
