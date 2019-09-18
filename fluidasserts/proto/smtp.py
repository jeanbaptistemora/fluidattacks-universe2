# -*- coding: utf-8 -*-

"""This module allows to check SMTP-specific vulnerabilities."""

# standard imports
import smtplib

# local imports
from fluidasserts import DAST, LOW, MEDIUM, _get_result_as_tuple_host_port
from fluidasserts.helper import banner
from fluidasserts.utils.decorators import api

# Constants
PORT = 25


@api(risk=MEDIUM, kind=DAST)
def has_vrfy(ip_address: str, port: int = PORT) -> tuple:
    """
    Check if IP has VRFY command enabled.

    :param ip_address: IP address to test.
    :param port: If necessary, specify port to connect to (default: 25).
    """
    server = smtplib.SMTP(ip_address, port)
    service = banner.SMTPService(port)
    fingerprint = service.get_fingerprint(ip_address)
    vrfy = server.verify('root')

    return _get_result_as_tuple_host_port(
        protocol='SMTP', host=ip_address, port=port,
        msg_open='Has VRFY command enabled',
        msg_closed='Has VRFY command disabled',
        open_if=502 not in vrfy,
        fingerprint=fingerprint)


@api(risk=LOW, kind=DAST)
def is_version_visible(ip_address: str, port: int = PORT,
                       payload: bool = None) -> tuple:
    """
    Check if banner is visible.

    :param ip_address: IP address to test.
    :param port: If necessary, specify port to connect to (default: 25).
    """
    service = banner.SMTPService(port, payload=payload)
    version = service.get_version(ip_address)
    fingerprint = service.get_fingerprint(ip_address)

    result: bool = bool(version)

    return _get_result_as_tuple_host_port(
        protocol='SMTP', host=ip_address, port=port, extra=payload,
        msg_open='Version is visible',
        msg_closed='Version is not visible',
        open_if=result,
        fingerprint=fingerprint)
