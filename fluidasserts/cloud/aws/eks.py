# -*- coding: utf-8 -*-

"""AWS cloud checks (EKS)."""

# std imports
# None

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, MEDIUM, LOW
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def allows_insecure_inbound_traffic(key_id: str,
                                    secret: str,
                                    client_kwargs: dict = None,
                                    retry: bool = True) -> tuple:
    """
    Check if EKS security groups allow access to ports other than 443 (HTTPS).

    Opening all ports in Amazon EKS security groups is not a good practice
    because it allows attackers to use port scanners to identify applications
    and services running in EKS clusters and exploit their vulnerabilities.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :param client_kwargs: boto3 client `kwargs <https://boto3.amazonaws.com/
      v1/documentation/api/latest/guide/session.html>`_.
    :returns: - ``OPEN`` if there are unencrypted AMIs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'EKS security groups allow access on ports other than TCP port 443.'
    msg_closed: str = 'EKS security groups only allow access by HTTPS.'
    vulns, safes = [], []
    clusters = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='eks',
        func='list_clusters',
        param='clusters',
        boto3_client_kwargs=client_kwargs,
        retry=retry,
    )
    for cluster in clusters:
        cluster_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='eks',
            func='describe_cluster',
            param='cluster',
            retry=retry,
            name=cluster,
            boto3_client_kwargs=client_kwargs)
        security_groups_ids = cluster_description['resourcesVpcConfig'][
            'securityGroupIds']
        security_groups = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='ec2',
            func='describe_security_groups',
            param='SecurityGroups',
            retry=retry,
            GroupIds=security_groups_ids,
            boto3_client_kwargs=client_kwargs)

        has_only_https = all([
            all(
                map(lambda r: r['FromPort'] == 443 and
                    r['FromPort'] == r['ToPort'],
                    group['IpPermissions'])) for group in security_groups
        ])

        (vulns if not has_only_https else safes).append(
            (cluster_description['arn'],
             ('Configure the cluster to allow inbound traffic only'
              ' on TCP port 443 (HTTPS).')))

    return _get_result_as_tuple(
        service='EKS',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_endpoints_publicly_accessible(key_id: str,
                                      secret: str,
                                      retry: bool = True,
                                      client_kwargs: dict = None) -> tuple:
    """
    Check if the API servers of the Kubernetes cluster are publicly accessible.

    Disable public access to your API server endpoint so that it is not
    accessible from the Internet.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :param client_kwargs: boto3 client `kwargs <https://boto3.amazonaws.com/
      v1/documentation/api/latest/guide/session.html>`_.
    :returns: - ``OPEN`` if there is a public Kubernetes API server.
                accessible.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`

    """
    msg_open: str = ('The endpoints of the Kubernetes API server of the EKS'
                     ' clusters are publicly accessible from the Internet')
    msg_closed: str = (
        'The endpoints of the Kubernetes API server of the EKS'
        ' clusters are not publicly accessible from the Internet')
    vulns, safes = [], []
    clusters = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='eks',
        func='list_clusters',
        param='clusters',
        boto3_client_kwargs=client_kwargs,
        retry=retry,
    )
    for cluster in clusters:
        cluster_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='eks',
            func='describe_cluster',
            param='cluster',
            retry=retry,
            name=cluster,
            boto3_client_kwargs=client_kwargs)
        vulnerable = (cluster_description['resourcesVpcConfig']
                      ['endpointPrivateAccess'] is False) and (
                          cluster_description['resourcesVpcConfig']
                          ['endpointPublicAccess'] is True)
        (vulns if vulnerable else safes).append(
            (cluster_description['arn'],
             ('The API Server must not be publicly accessible, it should only'
              ' be accessible from an AWS Virtual Private Cloud (VPC).')))

    return _get_result_as_tuple(
        service='EKS',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_disable_cluster_logging(key_id: str,
                                secret: str,
                                retry: bool = True,
                                client_kwargs: dict = None) -> tuple:
    """
    Check if control plane logging is enabled for AWS EKS clusters.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    :param client_kwargs: boto3 client `kwargs <https://boto3.amazonaws.com/
      v1/documentation/api/latest/guide/session.html>`_.
    :returns: - ``OPEN`` if there are EKS Clusters with control plane logging
                disabled.
                Encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'EkS clusters have control plane logging disabled.'
    msg_closed: str = 'EkS clusters have control plane logging enabled.'
    vulns, safes = [], []

    clusters = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='eks',
        func='list_clusters',
        param='clusters',
        boto3_client_kwargs=client_kwargs,
        retry=retry)

    for cluster in clusters:
        cluster_description = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='eks',
            func='describe_cluster',
            param='cluster',
            retry=retry,
            name=cluster,
            boto3_client_kwargs=client_kwargs)

        vulnerable = all(
            map(lambda x: x['enabled'] is False,
                cluster_description['logging']['clusterLogging']))
        (vulns if vulnerable else safes).append(
            (cluster_description['arn'],
             'Must enable control plane logging for the EKS Cluster.'))

    return _get_result_as_tuple(
        service='EKS',
        objects='Clusters',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
