# -*- coding: utf-8 -*-

"""AWS cloud checks (Generic)."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.utils.decorators import track, level, notify
from fluidasserts.helper import aws


@notify
@level('medium')
@track
def are_valid_credentials(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if given AWS credentials are working.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        identity = aws.get_caller_identity(key_id, secret, retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr:
        show_close('Given credentials are not valid.',
                   details=dict(key_id=key_id, secret=secret))
        return False
    else:
        show_open('Given credentials are valid.',
                  details=dict(identity=identity, key_id=key_id,
                               secret=secret))
        return True
