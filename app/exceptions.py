"""
    Implementacion de excepciones personalizadas para FluidIntegrates
"""


class SecureAccessException(Exception):
    """Excepcion que controla el acceso a recursos con autenticacion."""
    def __init__(self):
        """ Constructor """
        msg = "Excepcion - Acceso a recursos sin sesion activa"
        super(SecureAccessException, self).__init__(msg)


class SecureParamsException(Exception):
    """ Excepcion para controlar la validacion de parametros """
    def __init__(self):
        """ Constructor """
        msg = "Excepcion - Parametros incorrectos o faltantes"
        super(SecureParamsException, self).__init__(msg)


class APIConnectionException(Exception):
    """ Excepcion para controlar la comunicacion con el backend """
    def __init__(self):
        """ Constructor """
        msg = "Excepcion - Error de conexion con el servidor"
        super(APIConnectionException, self).__init__(msg)


class LogicException(Exception):
    """ Excepcion para controlar errores logicos generales """
    def __init__(self, code=99):
        """ Constructor """
        if code == 100:
            msg = "E100 - Usuario/incorrectos clave son obligatorios"
        elif code == 101:
            msg = "E101 - Otro"
        else:
            msg = "E102 - Error inesperado"
        super(LogicException, self).__init__(msg)
