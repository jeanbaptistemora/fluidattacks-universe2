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
