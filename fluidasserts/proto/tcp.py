# -*- coding: utf-8 -*-

"""This module allows to check TCP-specific vulnerabilities."""

# standard imports
import socket
from contextlib import suppress

# third party imports
import tlslite

# local imports
from fluidasserts import Unit, LOW, MEDIUM, DAST, OPEN, CLOSED
from fluidasserts.helper import ssl
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(OverflowError)
def is_port_open(ipaddress: str, port: int) -> tuple:
    """
    Check if a given port on an IP address is open.

    :param ipaddress: IP address to test.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if we are able to connect to the given IP Address and
                port using bare sockets.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Port is open'
    msg_closed: str = 'Port is closed'
    port_open: bool = False

    with suppress(socket.error):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ipaddress, port))
        port_open = True

    unit: Unit = Unit(where=f'{ipaddress}@{port}',
                      specific=[msg_open if port_open else msg_closed])

    if port_open:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.timeout, OverflowError, ConnectionRefusedError)
def is_port_insecure(ipaddress: str, port: int) -> tuple:
    """
    Check if a given port on an IP address is insecure.

    :param ipaddress: IP address to test.
    :param port: Port to connect to.
    :returns: - ``OPEN`` if we are not able to connect to the given IP Address
                and **port** using **TLS**.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Port does not support TLS'
    msg_closed: str = 'Port does support TLS'
    is_vulnerable: bool = True

    with suppress(tlslite.errors.TLSLocalAlert,
                  tlslite.errors.TLSIllegalParameterException):
        with ssl.connect(ipaddress, port):
            is_vulnerable = False

    unit: Unit = Unit(where=f'{ipaddress}@{port}',
                      specific=[msg_open if is_vulnerable else msg_closed])

    if is_vulnerable:
        return OPEN, msg_open, [unit], []
    return CLOSED, msg_closed, [], [unit]
