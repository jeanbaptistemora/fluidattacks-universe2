""" FluidIntegrates services definition """

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# pylint: disable=E0402
from . import util
# pylint: disable=E0402
from .dao import integrates_dao


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

def has_access_to_finding(allowed_findings, findingid, rol):
    """ Verify if the user has access to a finding submission. """
    hasAccess = False
    # Skip this check for admin users since they don't have any assigned projects
    if rol == 'admin':
        hasAccess = True
    else:
        for project in allowed_findings.keys():
            if findingid in allowed_findings[project]:
                hasAccess = True
                break
    return hasAccess

def is_customeradmin(project, email):
    """Verify if a user is a customeradmin."""
    project_data = integrates_dao.get_project_dynamo(project)
    for data in project_data:
        if 'customeradmin' in data:
            if email in data["customeradmin"]:
                return True
    return False
