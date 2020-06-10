# -*- coding: utf-8 -*-
"""AWS cloud checks (Redshift)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM, LOW
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _get_clusters(key_id, retry, secret, session_token):
    return aws.get_paginated_items(  # nosec
        key_id,
        retry,
        secret,
        session_token,
        'redshift',
        'describe_clusters',
        'MaxRecords',
        'Marker',
        'Clusters',
        next_token_name='NextMarker'
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_public_clusters(key_id: str,
                        secret: str,
                        session_token: str = None,
                        retry: bool = True) -> tuple:
    """
    Check if Redshift clusters are publicly accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Clusters are publicly accessible'
    msg_closed: str = 'Clusters are not publicly accessible'

    vulns, safes = [], []

    if clusters:
        for cluster in clusters:
            cluster_id = cluster['ClusterIdentifier']

            (vulns if cluster['PubliclyAccessible'] else safes).append(
                (cluster_id, 'Must not be publicly accessible'))

    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_encryption_disabled(key_id: str,
                            secret: str,
                            session_token: str = None,
                            retry: bool = True) -> tuple:
    """
    Check if Redshift clusters has encryption disabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are clusters with encryption disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Redshift clusters has encryption disabled.'
    msg_closed: str = 'Redshift clusters has encryption enabled.'

    vulns, safes = [], []

    for cluster in clusters:
        cluster_id = cluster['ClusterIdentifier']
        (vulns if not cluster['Encrypted'] else safes).append(
            (cluster_id, 'must has encryption enabled.'))

    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def uses_default_kms_key(key_id: str,
                         secret: str,
                         session_token: str = None,
                         retry: bool = True) -> tuple:
    """Check if Redshift clusters use default KMS key for encryption.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """

    kms_aliases = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        boto3_client_kwargs={'aws_session_token': session_token},
        service='kms',
        func='list_aliases',
        param='Aliases',
        retry=retry)

    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Redshift clusters use default KMS key.'
    msg_closed: str = 'Redshift clusters use default KMS key.'

    vulns, safes = [], []

    for cluster in clusters:
        vulnerable = False
        vol_key = cluster.get('KmsKeyId', '')
        if vol_key:
            for alias in kms_aliases:
                if alias.get('TargetKeyId', '') == vol_key.split("/")[1] \
                        and alias.get('AliasName') == "alias/aws/redshift":
                    vulnerable = True
            (vulns if vulnerable
             else safes).append(
                 (cluster['ClusterIdentifier'],
                  'uses default KMS key'))
    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_audit_logging_disabled(key_id: str,
                              secret: str,
                              session_token: str = None,
                              retry: bool = True) -> tuple:
    """Check if Redshift clusters have audit logging disabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """

    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Redshift clusters use default KMS key.'
    msg_closed: str = 'Redshift clusters use default KMS key.'

    vulns, safes = [], []

    for cluster in clusters:
        cluster_id = cluster['ClusterIdentifier']
        logging = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='redshift',
            func='describe_logging_status',
            boto3_client_kwargs={'aws_session_token': session_token},
            param='LoggingEnabled',
            ClusterIdentifier=cluster_id,
            retry=retry)

        (vulns if not logging
         else safes).append(
             (cluster_id,
              'uses default KMS key'))
    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_not_upgrade_allowed(key_id: str,
                           secret: str,
                           session_token: str = None,
                           retry: bool = True) -> tuple:
    """Check if Redshift clusters have version upgrading disabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """

    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Redshift clusters do not allow version upgrade.'
    msg_closed: str = 'Redshift clusters allow version upgrade.'

    vulns, safes = [], []

    for cluster in clusters:
        cluster_id = cluster['ClusterIdentifier']

        (vulns if not cluster.get('AllowVersionUpgrade', False)
         else safes).append(
             (cluster_id,
              'have Allow Version Upgrade disabled'))
    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_requires_ssl(key_id: str,
                     secret: str,
                     session_token: str = None,
                     retry: bool = True) -> tuple:
    """Check if Redshift clusters do not require use of SSL.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """

    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Redshift clusters do not require using SSL.'
    msg_closed: str = 'Redshift clusters require using SSL.'

    vulns, safes = [], []

    for cluster in clusters:
        vulnerable = False
        cluster_id = cluster['ClusterIdentifier']
        param_groups = cluster.get('ClusterParameterGroups', [])

        for group in param_groups:
            params = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='redshift',
                func='describe_cluster_parameters',
                boto3_client_kwargs={'aws_session_token': session_token},
                param='Parameters',
                ParameterGroupName=group['ParameterGroupName'],
                retry=retry)
            for param in params:
                if param['ParameterName'] == 'require_ssl' \
                        and param['ParameterValue'] == "false":
                    vulnerable = True
            (vulns if vulnerable
             else safes).append(
                 (f'{cluster_id}/{group["ParameterGroupName"]}',
                  'does not require SSL'))
    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_user_activity_logging_disabled(key_id: str,
                                      secret: str,
                                      session_token: str = None,
                                      retry: bool = True) -> tuple:
    """Check if Redshift clusters does not log user activity.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """

    clusters = _get_clusters(key_id, retry, secret, session_token)

    msg_open: str = 'Redshift clusters do not log user activity.'
    msg_closed: str = 'Redshift clusters log user activity.'

    vulns, safes = [], []

    for cluster in clusters:
        vulnerable = False
        cluster_id = cluster['ClusterIdentifier']
        param_groups = cluster.get('ClusterParameterGroups', [])

        for group in param_groups:
            params = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='redshift',
                func='describe_cluster_parameters',
                boto3_client_kwargs={'aws_session_token': session_token},
                param='Parameters',
                ParameterGroupName=group['ParameterGroupName'],
                retry=retry)
            for param in params:
                if param['ParameterName'] == 'enable_user_activity_logging' \
                        and param['ParameterValue'] == "false":
                    vulnerable = True
            (vulns if vulnerable
             else safes).append(
                 (f'{cluster_id}/{group["ParameterGroupName"]}',
                  'has user activity logging disabled'))
    return _get_result_as_tuple(
        service='RedShift',
        objects='clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
