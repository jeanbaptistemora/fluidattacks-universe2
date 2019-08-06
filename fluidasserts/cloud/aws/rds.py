# -*- coding: utf-8 -*-

"""AWS cloud checks (RDS)."""

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
@level('high')
@track
def has_public_instances(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if RDS DB instances are publicly accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        instances = aws.run_boto3_func(key_id, secret, 'rds',
                                       'describe_db_instances',
                                       param='DBInstances',
                                       retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not instances:
        show_close('Not RDS instances were found')
        return False

    result = [x for x in instances if x['PubliclyAccessible']]
    if result:
        show_open('RDS instances are publicly accessible',
                  details=dict(instances=result))
        return True
    show_close('RDS instances are not publicly accessible')
    return False
