# -*- coding: utf-8 -*-

"""This module allows to check Schneider Electric PowerLogic devices."""

# standard imports
# None

# third party imports
# None

# local imports
from fluidasserts import HIGH, DAST
from fluidasserts.helper import http
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=HIGH, kind=DAST)
@unknown_if(http.ConnError)
def pm800_has_default_credentials(url: str) -> tuple:
    """
    Check if PowerLogic PM800 has default credentials.

    :param url: URL of PM800 admin page.
    :returns: - ``OPEN`` if PM800 device has default credentials.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    default_creds = {
        ('Administrator', 'Gateway'),
        ('admin', '0'),
        ('8000', '0'),
        ('user1', 'pass1'),
        ('user2', 'pass2'),
        ('Guest', 'Guest')
    }
    working_creds = []
    for creds in default_creds:
        sess = http.HTTPSession(url, auth=creds)
        if sess.response.status_code == 200 and 'PM800' in sess.response.text:
            working_creds.append(creds)

    sess.set_messages(
        source='PM800/HTTPServer',
        msg_open='PowerLogic PM800 device has default credentials',
        msg_closed='PowerLogic PM800 device does not have default credentials'
    )

    sess.add_unit(is_vulnerable=working_creds, specific=working_creds)
    return sess.get_tuple_result()


@api(risk=HIGH, kind=DAST)
@unknown_if(http.ConnError)
def egx100_has_default_credentials(url: str) -> tuple:
    """
    Check if PowerLogic EGX100 has default credentials.

    :param url: URL of EGX100 admin page.
    :returns: - ``OPEN`` if EGX100 device has default credentials.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    default_creds = {
        ('Administrator', 'Gateway'),
        ('Guest', 'Guest')
    }
    working_creds = []
    for creds in default_creds:
        sess = http.HTTPSession(url, auth=creds)
        if sess.response.status_code == 200 and 'EGX100' in sess.response.text:
            working_creds.append(creds)
    sess.set_messages(
        source='PM800/HTTPServer',
        msg_open='PowerLogic EGX100 device has default credentials',
        msg_closed='PowerLogic EGX100 device does not have default credentials'
    )

    sess.add_unit(is_vulnerable=working_creds, specific=working_creds)
    return sess.get_tuple_result()
