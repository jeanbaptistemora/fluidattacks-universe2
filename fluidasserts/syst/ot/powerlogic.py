# -*- coding: utf-8 -*-

"""This module allows to check Schneider Electric PowerLogic devices."""

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
def pm800_has_default_credentials(host: str) -> bool:
    """
    Check if PowerLogic PM800 has default credentials.

    :param hostname: IP or host of phone.
    """
    default_creds = {
        ('Administrator', 'Gateway'),
        ('admin', '0'),
        ('8000', '0'),
        ('user1', 'user2'),
        ('user2', 'user2'),
        ('Guest', 'Guest')
    }
    working_creds = []
    for creds in default_creds:
        try:
            url = f'http://{host}'
            sess = http.HTTPSession(url, auth=creds)
        except http.ConnError as exc:
            show_unknown('Could not connect',
                         details=dict(hostname=host, url=url,
                                      reason=str(exc).replace(':', ',')))
            return False

        if sess.response.status_code == 200:
            working_creds.append(creds)
    if working_creds:
        show_open('PowerLogic PM800 device has default credentials',
                  details=dict(host=host, credentials=working_creds))
        return True
    show_close('PowerLogic PM800 device does not have default credentials',
               details=dict(host=host))
    return False
