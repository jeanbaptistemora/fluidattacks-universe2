""" Modulo de seguridad para FluidIntegrates """

from .exceptions import SecureAccessException
from .exceptions import SecureParamsException
from .exceptions import LogicException
import re

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

    def post_numeric(self, request, key_name, required=True):
        """ Verifica que un parametro tenga
            el formato de numero adecuado """
        value = self.post(request, key_name, required)
        if value.strip() == "":
            raise LogicException()
        elif not re.search("^[0-9]+$", name):
            raise LogicException("")

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
