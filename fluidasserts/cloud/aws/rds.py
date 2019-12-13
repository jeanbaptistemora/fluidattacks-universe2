# -*- coding: utf-8 -*-

"""AWS cloud checks (RDS)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, HIGH, MEDIUM, LOW
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_public_instances(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check if RDS DB instances are publicly accessible.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    instances = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='rds',
                                   func='describe_db_instances',
                                   param='DBInstances',
                                   retry=retry)

    msg_open: str = 'RDS instances are publicly accessible'
    msg_closed: str = 'RDS instances are not publicly accessible'

    vulns, safes = [], []

    if instances:
        for instance in instances:
            instance_arn = instance['DBInstanceArn']

            (vulns if instance['PubliclyAccessible'] else safes).append(
                (instance_arn, 'Must not be publicly accessible'))

    return _get_result_as_tuple(
        service='RDS', objects='instances',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_cluster_not_inside_a_db_subnet_group(key_id: str, secret: str,
                                            retry: bool = True) -> tuple:
    """
    Check if Database clusters are inside a DB Subnet Group.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    clusters = aws.run_boto3_func(key_id=key_id,
                                  secret=secret,
                                  service='rds',
                                  func='describe_db_clusters',
                                  param='DBClusters',
                                  retry=retry)

    msg_open: str = 'RDS clusters are not inside a database subnet group'
    msg_closed: str = 'RDS clusters are inside a database subnet group'

    vulns, safes = [], []

    if clusters:
        for cluster in clusters:
            cluster_arn = cluster['DBClusterArn']
            (vulns if 'DBSubnetGroup' not in cluster else safes).append(
                (cluster_arn, 'must be inside a database subnet group'))

    return _get_result_as_tuple(
        service='RDS', objects='clusters',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def is_instance_not_inside_a_db_subnet_group(key_id: str, secret: str,
                                             retry: bool = True) -> tuple:
    """
    Check if Database Instances are inside a DB Subnet Group.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    instances = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='rds',
                                   func='describe_db_instances',
                                   param='DBInstances',
                                   retry=retry)

    msg_open: str = 'RDS instances are not inside a database subnet group'
    msg_closed: str = 'RDS instances are inside a database subnet group'

    vulns, safes = [], []

    if instances:
        for instance in instances:
            instance_arn = instance['DBInstanceArn']

            (vulns if 'DBSubnetGroup' not in instance else safes).append(
                (instance_arn, 'must be inside a database subnet group'))

    return _get_result_as_tuple(
        service='RDS', objects='instances',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_encryption_disabled(key_id: str, secret: str,
                            retry: bool = True) -> tuple:
    """
    Check if the instances have `StorageEncrypted` disabled.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances with `StorageEncrypted`
                 disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'The instances are not encrypted.'
    msg_closed: str = 'The Instances are encrypted.'

    vulns, safes = [], []
    instances = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='rds',
                                   func='describe_db_instances',
                                   param='DBInstances',
                                   retry=retry)

    if instances:
        for instance in instances:
            (vulns if not instance['StorageEncrypted'] else safes).append(
                (instance['DBInstanceArn'],
                 ('Set the StorageEncrypted property to'
                  ' true to encrypt the instance.')))

    return _get_result_as_tuple(
        service='RDS',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=HIGH, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_public_snapshots(key_id: str, secret: str,
                         retry: bool = True) -> tuple:
    """
    Check for snapshots that allow public access.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are snapshots that allow public access.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Snapshots are publicly accessible.'
    msg_closed: str = 'Snapshots are not publicly accessible.'

    vulns, safes = [], []
    snapshots = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='rds',
        func='describe_db_snapshots',
        param='DBSnapshots',
        retry=retry)
    for snapshot in snapshots:
        snapshot = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='rds',
            func='describe_db_snapshot_attributes',
            param='DBSnapshotAttributesResult',
            DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'],
            retry=retry)
        vulnerable = any(
            list(
                map(lambda x: 'all' in x['AttributeValues'],
                    snapshot['DBSnapshotAttributes'])))

        (vulns if vulnerable else safes).append(
            (snapshot['DBSnapshotIdentifier'],
             'Disable public access from the snapshot.'))

    return _get_result_as_tuple(
        service='RDS',
        objects='Snapshots',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def not_uses_iam_authentication(key_id: str, secret: str,
                                retry: bool = True) -> tuple:
    """
    Check if the BD instances are not using IAM database authentication.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances that do not use IAM database
                 authentication.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Instances do not use IAM database authentication.'
    msg_closed: str = 'Instances use IAM database authentication.'

    vulns, safes = [], []
    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='rds',
        func='describe_db_instances',
        param='DBInstances',
        retry=retry)

    for instance in instances:
        (vulns if not instance['IAMDatabaseAuthenticationEnabled'] else
         safes).append((instance['DBInstanceArn'],
                        'Use IAM database authentication.'))

    return _get_result_as_tuple(
        service='RDS',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def unrestricted_db_security_groups(key_id: str,
                                    secret: str,
                                    retry: bool = True) -> tuple:
    """
    Check if the database security groups allow unrestricted access.

    AWS RDS DB security groups should not allow access from 0.0.0.0/0.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances that do not use IAM database
                 authentication.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'RDS DB security groups allow unrestricted access (0.0.0.0/0)'
    msg_closed: str = 'RDS DB security groups have restricted access.'

    vulns, safes = [], []
    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='rds',
        func='describe_db_instances',
        param='DBInstances',
        retry=retry)
    for instance in instances:
        security_groups_ids = list(
            map(lambda x: x['VpcSecurityGroupId'],
                instance['VpcSecurityGroups']))
        security_groups = aws.run_boto3_func(
            key_id,
            secret=secret,
            service='ec2',
            func='describe_security_groups',
            param='SecurityGroups',
            GroupIds=security_groups_ids,
            retry=retry)
        vulnerable = []
        for group in security_groups:
            ip_permissions = \
                group['IpPermissions'] + group['IpPermissionsEgress']

            is_vulnerable: bool = any(
                ip_range['CidrIp'] == '0.0.0.0/0'
                for ip_permission in ip_permissions
                for ip_range in ip_permission['IpRanges'])

            vulnerable.append(is_vulnerable)

        (vulns if any(vulnerable) else safes).append(
            (instance['DBInstanceArn'],
             'Restrict access to the required IP addresses only.'))

    return _get_result_as_tuple(
        service='RDS',
        objects='instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_not_deletion_protection(key_id: str, secret: str,
                                retry: bool = True) -> tuple:
    """
    Check if the database instances are not protected against deletion.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances no protected.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Instances are not protected against deletion.'
    msg_closed: str = 'Instances are protected against deletion.'

    vulns, safes = [], []

    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='rds',
        func='describe_db_instances',
        param='DBInstances',
        retry=retry)

    for instance in instances:
        (vulns if not instance['DeletionProtection'] else safes).append(
            (instance['DBInstanceArn'],
             'must enable deletion protection.'))
    return _get_result_as_tuple(
        service='RDS',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_disabled_automatic_backups(key_id: str,
                                   secret: str,
                                   retry: bool = True) -> tuple:
    """
    Check if the database instances has disabled automatic backups.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are instances with automatic backup disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Instances has automatic backups disabled.'
    msg_closed: str = 'Instances has automatic backups enabled.'

    vulns, safes = [], []

    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='rds',
        func='describe_db_instances',
        param='DBInstances',
        retry=retry)

    for instance in instances:
        (vulns if instance['BackupRetentionPeriod'] == 0 else safes).append(
            (instance['DBInstanceArn'], 'must enable automatic backups.'))
    return _get_result_as_tuple(
        service='RDS',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
