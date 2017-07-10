""" Definicion de servicios para FluidIntegrates """

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
# pylint: disable=E0402
from . import util
from .filter import FilterManager
# pylint: disable=E0402
from .exceptions import SecureParamsException
from .exceptions import LogicException
from .dao import integrates_dao


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """ Servicio definido para la autenticacion."""
    username = ""
    return util.response([], 'Bienvenido ' + username, False)


def get_company(user):
    """Obtiene la compania a la que pertenece el usuario."""
    return integrates_dao.get_company_dao(user)


def get_role(user):
    """Obtiene el rol que que tiene el usuario."""
    return integrates_dao.get_role_dao(user)


def is_registered(user):
    """Verifica si el usuario esta registrado."""
    return integrates_dao.is_registered_dao(user)


def has_access_to_project(user, project_name):
    """Verifica si el usuario tiene acceso al proyecto en cuestion."""
    if user.endswith('fluid.la'):
        return True
    return integrates_dao.has_access_to_project_dao(user, project_name)
