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
    test_user = 'customer@testcompany.com'
    test_pass = 'beethoahae2iH1teev4bu9ahd'
    test_company = 'TEST COMPANY'
    try:
        fmanager = FilterManager()
        username = fmanager.post(request, "user")
        password = fmanager.post(request, "pass")
        if username == test_user and password == test_pass:
            request.session['username'] = username
            request.session['company'] = test_company
            request.session['registered'] = '1'
            request.session['role'] = 'customer'
            integrates_dao.create_user_dao(username)
        else:
            fmanager.error(100)
    except (SecureParamsException, LogicException) as expt:
        return util.response([], str(expt), True)
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
