# -*- coding: utf-8 -*-

"""This module allows to check cameras vulnerabilities."""

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
def axis_has_rce(url: str) -> tuple:
    """
    Check if Axis Communications MPQT/PACS Server has RCE.

    Taken from https://www.exploit-db.com/exploits/40125

    :param url: URL of Axis camera.
    :returns: - ``OPEN`` if camera is vulnerable to RCE.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.
    :rtype: :class:`fluidasserts.Result`
    """
    url = f'{url}/httpDisabled.shtml?&http_user=%p|%p'
    sess = http.HTTPSession(url)

    sess.set_messages(
        source='Camera/HTTPServer',
        msg_open='Axis camera vulnerable to RCE',
        msg_closed='Axis camera not vulnerable to RCE'
    )

    sess.add_unit(is_vulnerable=sess.response.status_code == 500)

    return sess.get_tuple_result()
