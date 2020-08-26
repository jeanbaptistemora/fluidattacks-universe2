"""AWS cloud checks for ``ElastiCache```."""


# Third parties imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# Local imports
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts import DAST, SCA
from fluidasserts.helper import aws
from fluidasserts import LOW, MEDIUM, HIGH
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


@api(risk=MEDIUM, kind=SCA)
@unknown_if(BotoCoreError, RequestException)
def uses_unsafe_engine_version(key_id: str,
                               secret: str,
                               session_token: str = None,
                               retry: bool = True) -> tuple:
    """Check if an ``ElastiCache`` engine is a vulnerable version.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    versions_redis = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elasticache',
        func='describe_cache_engine_versions',
        param='CacheEngineVersions',
        Engine='redis',
        DefaultOnly=True,
        retry=retry)

    versions_memc = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elasticache',
        func='describe_cache_engine_versions',
        param='CacheEngineVersions',
        Engine='memcached',
        DefaultOnly=True,
        retry=retry)

    acceptable_redis = max(map(lambda x: x['EngineVersion'], versions_redis))
    acceptable_memc = max(map(lambda x: x['EngineVersion'], versions_memc))

    caches = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='elasticache',
        func='describe_cache_clusters',
        param='CacheClusters',
        retry=retry)

    msg_open: str = 'Elasticache clusters use an unsafe engine version'
    msg_closed: str = 'Elasticache clusters use the last engine version'

    vulns, safes = [], []
    for cluster in caches:
        (vulns if (cluster.get('Engine') == 'memcached'
                   and not cluster.get('EngineVersion') == acceptable_memc)
         or (cluster.get('Engine') == 'redis'
             and not cluster.get('EngineVersion') == acceptable_redis)
         else safes).append(
             (f'{cluster["CacheClusterId"]}/{cluster["EngineVersion"]}',
              'uses unsafe engine version'))

    return _get_result_as_tuple(
        service='Elasticache',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_transit_encryption_disabled(key_id: str,
                                   secret: str,
                                   session_token: str = None,
                                   retry: bool = True) -> tuple:
    """Check if an ``ElastiCache`` cluster has transit encryption disabled.

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

    msg_open: str = 'Elasticache clusters have transit encryption disabled'
    msg_closed: str = ('Elasticache clusters do not have transit '
                       'encryption disabled')

    vulns, safes = [], []
    for cluster in caches:
        (vulns if cluster.get('Engine') == 'redis'
         and not cluster.get('TransitEncryptionEnabled', '') == "True"
         else safes).append(
             (cluster['CacheClusterId'],
              'has transit encryption disabled'))

    return _get_result_as_tuple(
        service='Elasticache',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_at_rest_encryption_disabled(key_id: str,
                                   secret: str,
                                   session_token: str = None,
                                   retry: bool = True) -> tuple:
    """Check if an ``ElastiCache`` cluster has at rest encryption disabled.

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

    msg_open: str = 'Elasticache clusters have at rest encryption disabled'
    msg_closed: str = ('Elasticache clusters do not have at rest '
                       'encryption disabled')

    vulns, safes = [], []
    for cluster in caches:
        (vulns if cluster.get('Engine') == 'redis'
         and not cluster.get('AtRestEncryptionEnabled', '') == "True"
         else safes).append(
             (cluster['CacheClusterId'],
              'has At Rest encryption disabled'))

    return _get_result_as_tuple(
        service='Elasticache',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
