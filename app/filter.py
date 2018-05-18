"""Security module for FluidIntegrates."""

# pylint: disable=E0402
from .exceptions import SecureAccessException
from .exceptions import SecureParamsException
from .exceptions import LogicException
import re


class FilterManager(object):
    """ Class to manage the HTTP entries of Integrates. """

    def has_session(self, request):
        """ Check if there is an active session in the system. """
        if "username" not in request.session:
            raise SecureAccessException()
        if request.session["username"] is None:
            raise SecureAccessException()

    def post(self, request, key_name, required=True):
        """ Gets a POST parameter validating if it is required. """
        parameter = request.POST.get(key_name, "")
        if required:
            if parameter == "":
                raise SecureParamsException()
        return parameter

    def post_numeric(self, request, key_name, required=True):
        """ Verify the appropriate number format of a parameter. """
        value = self.post(request, key_name, required)
        if value.strip() == "":
            raise LogicException()
        elif not re.search("^[0-9]+$", key_name):
            raise LogicException("")

    def get(self, request, key_name, required=True):
        """ Gets a GET parameter validating if it is required. """
        parameter = request.GET.get(key_name, "")
        if required:
            if parameter == "":
                raise SecureParamsException()
        return parameter

    def error(self, code):
        """ Invoke the exception of general errors. """
        raise LogicException(code)
