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
    " Servicio definido para la autenticacion "
    username = ""
    try:
        fmanager = FilterManager()
        username = fmanager.post(request, "user")
        password = fmanager.post(request, "pass")
        if not OneLoginAPI(username, password).login():
            fmanager.error(100)
    except (SecureParamsException, LogicException) as expt:
        return util.response([], str(expt), True)
    request.session['username'] = username
    return util.response([], 'Bienvenido ' + username, False)
