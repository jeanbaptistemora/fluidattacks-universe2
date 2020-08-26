# -*- coding: utf-8 -*-

"""This module allows to check ``LDAP`` vulnerabilities."""

# standard imports
from contextlib import suppress

# 3rd party imports
from ldap3 import Server
from ldap3 import Connection
from ldap3.core.exceptions import LDAPExceptionError, LDAPSocketOpenError

# local imports
from fluidasserts import DAST, HIGH, _get_result_as_tuple_host_port
from fluidasserts.utils.decorators import unknown_if, api

PORT = 389
SSL_PORT = 636


@api(risk=HIGH, kind=DAST)
@unknown_if(LDAPSocketOpenError)
def is_anonymous_bind_allowed(ldap_server: str, port: int = PORT) -> tuple:
    """
    Check whether anonymous binding is allowed on LDAP server.

    :param ldap_server: LDAP server address to test.
    :param port: If necessary, specify port to connect to.
    """
    anonymous_bonded: bool = False

    with suppress(LDAPExceptionError):
        try:
            server = Server(ldap_server)
            conn = Connection(server)
        finally:
            conn.unbind()

        if conn.bind() is True:
            anonymous_bonded = True

    return _get_result_as_tuple_host_port(
        protocol='LDAP', host=ldap_server, port=port,
        msg_open='LDAP anonymous bind is possible',
        msg_closed='LDAP anonymous bind is not possible',
        open_if=anonymous_bonded)
