# -*- coding: utf-8 -*-

"""This module allows to check cameras vulnerabilities."""

# standard imports
# None

# third party imports
# None

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import http
from fluidasserts.utils.decorators import track, level, notify


@notify
@level('high')
@track
def axis_has_rce(cam_ip: str) -> bool:
    """
    Check if Axis Communications MPQT/PACS Server has RCE.

    Taken from https://www.exploit-db.com/exploits/40125

    :param cam_ip: IP or host of Axis camera.
    """
    try:
        url = 'http://{}/httpDisabled.shtml?&http_user=%p|%p'.format(cam_ip)
        sess = http.HTTPSession(url)
    except http.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(cam_ip=cam_ip,
                                  reason=str(exc).replace(':', ',')))
        return False

    if sess.response.status_code == 500:
        show_open('Axis camera vulnerable to RCE', details=dict(cam_ip=cam_ip))
        return True
    show_close('Axis camera not vulnerable to RCE',
               details=dict(cam_ip=cam_ip))
    return False
