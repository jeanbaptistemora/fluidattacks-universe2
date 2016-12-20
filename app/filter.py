""" Modulo de seguridad para FluidIntegrates """

from .exceptions import SecureAccessException
from .exceptions import SecureParamsException
from .exceptions import LogicException

class FilterManager(object):
    """ Clase para administrar las entradas HTTP de Integrates """

    def has_session(self, request):
        """ Verifica si existe una sesion en el sistema"""
        if "username" not in request.session:
            raise SecureAccessException()
        if request.session["username"] is None:
            raise SecureAccessException()

    def post(self, request, key_name, required=True):
        """ Obtiene un parametro post validando si es obligatorio"""
        parameter = request.POST.get(key_name, "")
        if required:
            if parameter == "":
                raise SecureParamsException()
        return parameter

    def get(self, request, key_name, required=True):
        """ Obtiene un parametro post validando si es obligatorio"""
        parameter = request.GET.get(key_name, "")
        if required:
            if parameter == "":
                raise SecureParamsException()
        return parameter

    def error(self, code):
        """ Invoca la excepcion de errores generales """
        raise LogicException(code)
