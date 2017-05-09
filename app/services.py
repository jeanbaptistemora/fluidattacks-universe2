""" Definicion de servicios para FluidIntegrates """

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import util
from .filter import FilterManager
from .exceptions import SecureParamsException
from .exceptions import LogicException
from .models import OneLoginAPI


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """ Servicio definido para la autenticacion."""
    username = ""
    try:
        fmanager = FilterManager()
        username = fmanager.post(request, "user")
        password = fmanager.post(request, "pass")
        if not OneLoginAPI(username, password).login():
            # FIXME: This is only for testing purposes
            test_user = 'customer@bancolombia.com.co'
            test_pass = 'yaech2saiFooh5Ahz4yaig5al'
            test_company = 'Bancolombia'
            test_role = 'customer'
            if username == test_user and password == test_pass:
                request.session['username'] = username
                request.session['company'] = get_company(username)
                request.session['role'] = test_role
                request.session['registered'] = is_registered(username)
            else:
                fmanager.error(100)
        else:
            request.session['username'] = username
            request.session['company'] = get_company(username)
            request.session['registered'] = is_registered(username)
            request.session['role'] = get_role(username)
    except (SecureParamsException, LogicException) as expt:
        return util.response([], str(expt), True)
    return util.response([], 'Bienvenido ' + username, False)


def get_company(user):
    """Obtiene la compania a la que pertenece el usuario."""
    return 'FLUID'


def get_role(user):
    """Obtiene el rol que que tiene el usuario."""
    return 'admin'


def is_registered(user):
    """Verifica si el usuario esta registrado."""
    return 'True'


def has_access_to_project(user, projectname):
    """Verifica si el usuario tiene acceso al proyecto en cuestion."""
    return True
