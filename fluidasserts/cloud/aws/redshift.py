# -*- coding: utf-8 -*-

"""AWS cloud checks (Redshift)."""

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
def has_public_clusters(key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if Redshift clusters are publicly accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        clusters = aws.run_boto3_func(key_id, secret, 'redshift',
                                      'describe_clusters',
                                      param='Clusters',
                                      retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not clusters:
        show_close('Not clusters were found')
        return False

    result = False
    for cluster in clusters:
        if cluster['PubliclyAccessible']:
            show_open('Cluster is publicly accessible',
                      details=dict(cluster=cluster))
            result = True
        else:
            show_close('Cluster is not publicly accessible',
                       details=dict(cluster=cluster))
    return result
