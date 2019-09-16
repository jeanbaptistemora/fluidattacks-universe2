# -*- coding: utf-8 -*-

"""AWS cloud checks (Redshift)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_public_clusters(key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if Redshift clusters are publicly accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    clusters = aws.run_boto3_func(key_id=key_id,
                                  secret=secret,
                                  service='redshift',
                                  func='describe_clusters',
                                  param='Clusters',
                                  retry=retry)

    msg_open: str = 'Clusters are publicly accessible'
    msg_closed: str = 'Clusters are not publicly accessible'

    vulns, safes = [], []

    if clusters:
        for cluster in clusters:
            cluster_id = cluster['ClusterIdentifier']

            (vulns if cluster['PubliclyAccessible'] else safes).append(
                (cluster_id, 'must not be publicly accessible'))

    return _get_result_as_tuple(
        service='RedShift', objects='clusters',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
