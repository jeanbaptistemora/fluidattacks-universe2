# -*- coding: utf-8 -*-

"""AWS cloud checks (EC2)."""

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException

# local imports
from fluidasserts import DAST, LOW, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _check_port_in_seggroup(port: int, group: dict) -> list:
    """Check if port is open according to security group."""
    vuln = []
    for perm in group['IpPermissions']:
        try:
            vuln += [perm for x in perm['IpRanges']
                     if x['CidrIp'] == '0.0.0.0/0' and
                     perm['FromPort'] <= port <= perm['ToPort']]
        except KeyError:
            pass
    return vuln


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def seggroup_allows_anyone_to_admin_ports(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if security groups allows connection from anyone to SSH service.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        2438,  # Oracle
        3306,  # MySQL
        3389,  # RDP
        5432,  # Postgres
        6379,  # Redis
        7199,  # Cassandra
        8111,  # DAX
        8888,  # Cassandra
        9160,  # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
    }

    security_groups = aws.run_boto3_func(key_id=key_id,
                                         secret=secret,
                                         service='ec2',
                                         func='describe_security_groups',
                                         param='SecurityGroups',
                                         retry=retry)

    msg_open: str = 'Security group allows connections to admin_ports'
    msg_closed: str = 'Security group denies connections to admin_ports'

    vulns, safes = [], []

    if security_groups:
        for group in security_groups:
            group_id = group['GroupId']
            for port in admin_ports:
                is_vulnerable: bool = _check_port_in_seggroup(port, group)

                (vulns if is_vulnerable else safes).append(
                    f'Security group {group_id} ' +
                    f'must deny connections to port {port}')

    return _get_result_as_tuple(
        service='EC2', objects='security groups',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def default_seggroup_allows_all_traffic(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if default security groups allows connection to or from anyone.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    security_groups = aws.run_boto3_func(key_id=key_id,
                                         secret=secret,
                                         service='ec2',
                                         func='describe_security_groups',
                                         param='SecurityGroups',
                                         retry=retry)

    msg_open: str = \
        'Default security groups allows connections from/to anyone'
    msg_closed: str = \
        'Default security groups does not allow connections from/to anyone'

    vulns, safes = [], []

    if security_groups:
        for group in security_groups:
            if not group['GroupName'] == 'default':
                continue

            group_id = group['GroupId']

            ip_permissions = \
                group['IpPermissions'] + group['IpPermissionsEgress']

            is_vulnerable: bool = any(
                ip_range['CidrIp'] == '0.0.0.0/0'
                for ip_permission in ip_permissions
                for ip_range in ip_permission['IpRanges'])

            (vulns if is_vulnerable else safes).append(
                f'Default security group {group_id} ' +
                f'must not have 0.0.0.0/0 CIDRs')

    return _get_result_as_tuple(
        service='EC2', objects='security groups',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_volumes(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if there are unencrypted volumes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    volumes = aws.run_boto3_func(key_id=key_id,
                                 secret=secret,
                                 service='ec2',
                                 func='describe_volumes',
                                 param='Volumes',
                                 retry=retry)

    msg_open: str = 'Account have non-encrypted volumes'
    msg_closed: str = 'All volumes are encrypted'

    vulns, safes = [], []

    if volumes:
        for volume in volumes:
            volume_id = volume['VolumeId']
            (vulns if not volume['Encrypted'] else safes).append(
                f'Volume {volume_id} must be encrypted')

    return _get_result_as_tuple(
        service='EC2', objects='volumes',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unencrypted_snapshots(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if there are unencrypted snapshots.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    identity = aws.run_boto3_func(key_id=key_id,
                                  secret=secret,
                                  service='sts',
                                  func='get_caller_identity',
                                  retry=retry)
    snapshots = aws.run_boto3_func(key_id=key_id,
                                   secret=secret,
                                   service='ec2',
                                   func='describe_snapshots',
                                   param='Snapshots',
                                   OwnerIds=[identity['Account']],
                                   retry=retry)

    msg_open: str = 'Account have non-encrypted snapshots'
    msg_closed: str = 'All snapshots are encrypted'

    vulns, safes = [], []

    if snapshots:
        for snapshot in snapshots:
            snapshot_id = snapshot['SnapshotId']
            (vulns if not snapshot['Encrypted'] else safes).append(
                f'Snapshot {snapshot_id} must be encrypted')

    return _get_result_as_tuple(
        service='EC2', objects='snapshots',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unused_seggroups(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if there are unused security groups.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    security_groups = aws.run_boto3_func(key_id=key_id,
                                         secret=secret,
                                         service='ec2',
                                         func='describe_security_groups',
                                         param='SecurityGroups',
                                         retry=retry)

    msg_open: str = 'Some security groups are not being used'
    msg_closed: str = 'All security groups are being used'

    vulns, safes = [], []

    if security_groups:
        for group in security_groups:
            group_id = group['GroupId']
            net_interfaces = aws.run_boto3_func(key_id=key_id,
                                                secret=secret,
                                                service='ec2',
                                                func=('describe_'
                                                      'network_interfaces'),
                                                param='NetworkInterfaces',
                                                Filters=[{
                                                    'Name': 'group-id',
                                                    'Values': [
                                                        group['GroupId'],
                                                    ]
                                                }],
                                                retry=retry)

            (vulns if not net_interfaces else safes).append(
                f'Security group {group_id} must be used or deleted')

    return _get_result_as_tuple(
        service='EC2', objects='security groups',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def vpcs_without_flowlog(
        key_id: str, secret: str, retry: bool = True) -> tuple:
    """
    Check if VPCs have flow logs.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    virtual_clouds = aws.run_boto3_func(key_id=key_id,
                                        secret=secret,
                                        service='ec2',
                                        func='describe_vpcs',
                                        param='Vpcs',
                                        Filters=[{
                                            'Name': 'state',
                                            'Values': ['available']
                                        }],
                                        retry=retry)

    msg_open: str = 'No Flow Logs found for VPC'
    msg_closed: str = 'Flow Logs found for VPC'

    vulns, safes = [], []

    if virtual_clouds:
        for cloud in virtual_clouds:
            cloud_id = cloud['VpcId']
            net_interfaces = aws.run_boto3_func(key_id=key_id,
                                                secret=secret,
                                                service='ec2',
                                                func='describe_flow_logs',
                                                param='FlowLogs',
                                                Filters=[{
                                                    'Name': 'resource-id',
                                                    'Values': [cloud_id],
                                                }],
                                                retry=retry)

            (vulns if not net_interfaces else safes).append(
                f'VPC {cloud_id} must be used or deleted')

    return _get_result_as_tuple(
        service='EC2', objects='virtual private clouds',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
