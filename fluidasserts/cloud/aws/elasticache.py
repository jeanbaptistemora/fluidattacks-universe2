"""AWS cloud checks for ``ElastiCache```."""


# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST
from fluidasserts.helper import aws
from fluidasserts import LOW
from fluidasserts.utils.decorators import api
from fluidasserts.utils.decorators import unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_port(key_id: str,
                      secret: str,
                      session_token: str = None,
                      retry: bool = True) -> tuple:
    """Check if an ``ElastiCache`` cluster uses a default port.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    caches = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elasticache',
        func='describe_cache_clusters',
        param='CacheClusters',
        retry=retry)

    msg_open: str = 'Elasticache clusters use default ports'
    msg_closed: str = 'Elasticache clusters do not use default ports'

    vulns, safes = [], []
    for cluster in caches:
        (vulns if (cluster.get('Engine') == 'memcached'
                   and cluster.get('ConfigurationEndpoint')['Port'] == 11211)
         or (cluster.get('Engine') == 'memcached'
             and cluster.get('ConfigurationEndpoint')['Port'] == 6379)
         else safes).append(
             (cluster['CacheClusterId'],
              'uses default port'))

    return _get_result_as_tuple(
        service='Elasticache',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
