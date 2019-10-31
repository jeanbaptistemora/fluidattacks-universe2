# -*- coding: utf-8 -*-

"""AWS cloud checks (EC2)."""

# std imports
from contextlib import suppress

# 3rd party imports
from botocore.exceptions import BotoCoreError
from botocore.vendored.requests.exceptions import RequestException
import numpy as np

# local imports
from fluidasserts import DAST, LOW, MEDIUM
from fluidasserts.helper import aws
from fluidasserts.cloud.aws import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


def _check_port_in_seggroup(port: int, group: dict) -> list:
    """Check if port is open according to security group."""
    vuln = []
    for perm in group['IpPermissions']:
        with suppress(KeyError):
            if perm['FromPort'] <= port <= perm['ToPort']:
                vuln += [perm for x in perm['IpRanges']
                         if x['CidrIp'] == '0.0.0.0/0']
                vuln += [perm for x in perm['Ipv6Ranges']
                         if x['CidrIp'] == '::/0']
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
        22,    # SSH
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
        445,    # CIFS
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
                    (group_id, f'Must deny connections to port {port}'))

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
                (group_id, 'Must not have 0.0.0.0/0 CIDRs'))

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
                (volume_id, 'Must be encrypted'))

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
                (snapshot_id, 'Must be encrypted'))

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
                (group_id, 'Must be used or deleted'))

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
                (cloud_id, 'Must be used or deleted'))

    return _get_result_as_tuple(
        service='EC2', objects='virtual private clouds',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_instances_using_unapproved_amis(key_id: str,
                                        secret: str,
                                        retry: bool = True) -> tuple:
    """
    Check if there are instances using approved Amazon Machine Images.

    To follow best practices use gold AMIs to create new instances of EC2.
    A golden AMI is an AMI that contains the latest security patches, software,
    configuration, security maintenance, and performance monitoring.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """
    msg_open: str = ('Instances are being launched using '
                     'unapproved Amazon Machine Images.')
    msg_closed: str = ('Instances are being launched using '
                       'approved Amazon Machine Images.')
    vulns, safes = [], []

    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_instances',
        param='Reservations',
        retry=retry,
    )

    for i in map(lambda x: x['Instances'], instances):
        for j in i:
            images = aws.run_boto3_func(
                key_id=key_id,
                secret=secret,
                service='ec2',
                func='describe_images',
                param='Images',
                retry=retry,
                ImageIds=[j['ImageId']])

            (vulns
             if images[0]['ImageOwnerAlias'] != 'amazon' else safes).append(
                 (j['InstanceId'], 'Base image must be approved by Amazon.'))

    return _get_result_as_tuple(
        service='EC2',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_insecure_port_range_in_security_group(key_id: str,
                                              secret: str,
                                              retry: bool = True) -> tuple:
    """
    Check if security groups implement range of ports to allow inbound traffic.

    Establishing a range of ports within security groups is not a good
    practice, because attackers can use port scanners to identify what services
    are running in instances.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """
    msg_open: str = 'Security group have port ranges established.'
    msg_closed: str = 'Security group do not have port ranges established.'
    vulns, safes = [], []

    security_groups = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_security_groups',
        param='SecurityGroups',
        retry=retry)
    for group in security_groups:
        vulnerable = []

        for rule in group['IpPermissions']:
            with suppress(KeyError):
                vulnerable.append(rule['FromPort'] != rule['ToPort'])

        vulnerable = any(vulnerable)
        (vulns if vulnerable else safes).append(
            (group['GroupId'],
             'The security group should not implement a range of ports.'))

    return _get_result_as_tuple(
        service='EC2',
        objects='Security Groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unrestricted_dns_access(key_id: str, secret: str,
                                retry: bool = True) -> tuple:
    """
    Check if inbound rules that allow unrestricted access to port 53.

    TCP/UDP port 53 is used by the Domain Name Service during DNS resolution.
    Restrict access to TCP and UDP port 53 only those IP addresses that
    require, to implement the principle of least privilege and reduce the
    possibility of a attack.

    Allowing unrestricted  to DNS access can give chance of an attack such as
    Denial of Services (DOS) or Distributed Denial of Service Syn Flood (DDoS).

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """
    msg_open: str = 'Security groups allow access to DNS without restrictions.'
    msg_closed: str = ('Security groups allow access to DNS to'
                       ' the necessary IP addresses.')
    vulns, safes = [], []

    filters = [{'Name': 'ip-permission.protocol', 'Values': ['tcp', 'udp']}]

    security_groups = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_security_groups',
        param='SecurityGroups',
        retry=retry,
        Filters=filters)
    for group in security_groups:
        vulnerable = _check_port_in_seggroup(85, group)
        (vulns if vulnerable else safes).append(
            (group['GroupId'], ('Group must restrict access to TCP port'
                                ' and UDP 53 to the necessary IP addresses.')))
    return _get_result_as_tuple(
        service='EC2',
        objects='Security Groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_instances_using_iam_roles(key_id: str, secret: str,
                                  retry: bool = True) -> tuple:
    """
    Check if EC2 instances uses IAM Roles Profiles instead of IAM Access Keys.

    Use IAM roles instead of IAM Access Keys to appropriately grant access
    permissions to any application that perform AWS API requests running on
    your EC2 instances. With IAM roles you can avoid sharing long-term
    credentials and protect your instances from unauthorized access.

    See https://docs.aws.amazon.com/es_es/AWSEC2/latest/UserGuide/iam-roles
    -for-amazon-ec2.html

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.
    """
    msg_open: str = 'Instances are not using IAM roles.'
    msg_closed: str = 'Instances are using IAM roles.'
    vulns, safes = [], []
    instances = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_instances',
        param='Reservations',
        retry=retry)

    instances = np.array(list(map(lambda x: x['Instances'],
                                  instances))).flatten().tolist()

    for i in instances:
        (vulns if 'IamInstanceProfile' not in i.keys() else safes).append(
            (i['InstanceId'], 'Instance must use an IAM role.'))

    return _get_result_as_tuple(
        service='EC2',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unused_ec2_key_pairs(key_id: str, secret: str,
                             retry: bool = True) -> tuple:
    """
    Check if there are unused EC2 key pairs.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are unused EC2 key pairs.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'There are unused EC2 key pairs.'
    msg_closed: str = 'All EC2 key pairs are in use.'
    vulns, safes = [], []

    key_pairs = map(lambda x: x['KeyName'],
                    aws.run_boto3_func(
                        key_id=key_id,
                        secret=secret,
                        service='ec2',
                        func='describe_key_pairs',
                        param='KeyPairs',
                        retry=retry))
    for key in key_pairs:
        filters = [{
            'Name': 'instance-state-name',
            'Values': ['running']
        }, {
            'Name': 'key-name',
            'Values': [key]
        }]

        instances = aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='ec2',
            func='describe_instances',
            param='Reservations',
            retry=retry,
            Filters=filters)
        (vulns if not instances else safes).append(
            (key, 'The EC2 key pair is not in use, it must be removed.'))
    return _get_result_as_tuple(
        service='EC2',
        objects='Key Pairs',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_unrestricted_ftp_access(key_id: str, secret: str,
                                retry: bool = True) -> tuple:
    """
    Check security groups allow unrestricted access to TCP ports 20 and 21.

    Restrict access to TCP ports 20 y 21 to only IP addresses that require,
    it in order to implement the principle of least privilege.
    TCP ports 20 and 21 are used for data transfer and communication by the
    File Transfer Protocol (FTP) client-server applications:

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if FTP access is allowed without restrictions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Security groups allow access to ftp without restrictions.'
    msg_closed: str = ('Security groups allow access to ftp to'
                       ' the necessary IP addresses.')
    vulns, safes = [], []

    filters = [{'Name': 'ip-permission.protocol', 'Values': ['tcp']}]
    security_groups = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service='ec2',
        func='describe_security_groups',
        param='SecurityGroups',
        retry=retry,
        Filters=filters)
    for group in security_groups:
        vulnerable = any([_check_port_in_seggroup(i, group) for i in [20, 21]])
        (vulns if vulnerable else safes).append(
            (group['GroupId'],
             'Group must restrict access only to the necessary IP addresses.'))

    return _get_result_as_tuple(
        service='EC2',
        objects='Security Groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(BotoCoreError, RequestException)
def has_default_security_groups_in_use(key_id: str,
                                       secret: str,
                                       retry: bool = True) -> tuple:
    """
    Check if default security groups are in use.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if there are default security groups in use.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Default security groups are in use.'
    msg_closed: str = 'Default security groups are not in use.'
    vulns, safes = [], []

    instances = map(
        lambda x: x['Instances'],
        aws.run_boto3_func(
            key_id=key_id,
            secret=secret,
            service='ec2',
            func='describe_instances',
            param='Reservations',
            retry=retry))

    instances = np.array(list(instances)).flatten().tolist()
    for instance in instances:
        security_groups = map(lambda x: x['GroupName'],
                              instance['SecurityGroups'])
        (vulns if 'default' in security_groups else safes).append(
            (instance['InstanceId'],
             ('This instance use a default security'
              ' group, specify a custom security group.')))

    return _get_result_as_tuple(
        service='EC2',
        objects='Instances',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
