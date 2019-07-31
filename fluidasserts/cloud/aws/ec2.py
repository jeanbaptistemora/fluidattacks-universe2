# -*- coding: utf-8 -*-

"""AWS cloud checks (EC2)."""

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


@notify
@level('medium')
@track
def seggroup_allows_anyone_to_admin_ports(
        key_id: str, secret: str, retry: bool = True) -> bool:
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
    try:
        sec_groups = aws.run_boto3_func(key_id, secret, 'ec2',
                                        'describe_security_groups',
                                        param='SecurityGroups',
                                        retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not sec_groups:
        show_close('Not security groups were found')
        return False

    result = False

    for group in sec_groups:
        for admin_port in admin_ports:
            vuln = _check_port_in_seggroup(admin_port, group)
            if vuln:
                show_open(f'Security group allows connections \
from anyone to {admin_port}',
                          details=dict(group=group['Description'],
                                       ip_ranges=vuln))
                result = True
            else:
                show_close(f'Security group not allows connections \
from anyone to port {admin_port}',
                           details=dict(group=group['Description']))
    return result


@notify
@level('medium')
@track
def default_seggroup_allows_all_traffic(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if default security groups allows connection to or from anyone.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        sec_groups = aws.run_boto3_func(key_id, secret, 'ec2',
                                        'describe_security_groups',
                                        param='SecurityGroups',
                                        retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not sec_groups:
        show_close('Not security groups were found')
        return False

    result = False

    def_groups = filter(lambda x: x['GroupName'] == 'default', sec_groups)

    for group in def_groups:
        for ip_perm in group['IpPermissions'] + group['IpPermissionsEgress']:
            vuln = [ip_perm for x in ip_perm['IpRanges']
                    if x['CidrIp'] == '0.0.0.0/0']
        if vuln:
            show_open('Default security groups allows connections \
to or from anyone',
                      details=dict(group=group['Description'],
                                   ip_ranges=vuln))
            result = True
        else:
            show_close('Default security groups not allows connections \
to or from anyone',
                       details=dict(group=group['Description']))

    return result


@notify
@level('medium')
@track
def has_unencrypted_volumes(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if there are unencrypted volumes.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        volumes = aws.run_boto3_func(key_id, secret, 'ec2',
                                     'describe_volumes',
                                     param='Volumes',
                                     retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not volumes:
        show_close('Not volumes found')
        return False

    result = False

    for volume in volumes:
        if not volume['Encrypted']:
            show_open('Volume is not encrypted', details=dict(volume=volume))
            result = True
        else:
            show_close('Volume is encrypted', details=dict(volume=volume))
    return result


@notify
@level('medium')
@track
def has_unencrypted_snapshots(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if there are unencrypted snapshots.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        identity = aws.run_boto3_func(key_id, secret, 'sts',
                                      'get_caller_identity',
                                      retry=retry)
        snapshots = aws.run_boto3_func(key_id, secret, 'ec2',
                                       'describe_snapshots',
                                       param='Snapshots',
                                       retry=retry,
                                       OwnerIds=[identity['Account']])
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not snapshots:
        show_close('Not snapshots found')
        return False

    result = False

    for snapshot in snapshots:
        if not snapshot['Encrypted']:
            show_open('Snapshot is not encrypted',
                      details=dict(snapshot=snapshot))
            result = True
        else:
            show_close('Snapshot is encrypted',
                       details=dict(snapshot=snapshot))
    return result


@notify
@level('low')
@track
def has_unused_seggroups(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if there are unused security groups.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        seggroups = aws.run_boto3_func(key_id, secret, 'ec2',
                                       'describe_security_groups',
                                       param='SecurityGroups',
                                       retry=retry)
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not seggroups:
        show_close('Not security groups found')
        return False

    result = False

    for group in seggroups:
        net_ifaces = aws.run_boto3_func(key_id, secret, 'ec2',
                                        'describe_network_interfaces',
                                        param='NetworkInterfaces',
                                        retry=retry,
                                        Filters=[{'Name': 'group-id',
                                                  'Values':
                                                  [group['GroupId']]}])
        if not net_ifaces:
            show_open('Security group is not used',
                      details=dict(security_group=group['GroupId']))
            result = True
        else:
            show_close('Security group is being used',
                       details=dict(security_group=group['GroupId'],
                                    net_interfaces=net_ifaces))
    return result


@notify
@level('low')
@track
def vpcs_without_flowlog(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if VPCs have flow logs.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        vpcs = aws.run_boto3_func(key_id, secret, 'ec2',
                                  'describe_vpcs',
                                  param='Vpcs',
                                  retry=retry,
                                  Filters=[{'Name': 'state',
                                            'Values':
                                            ['available']}])
    except aws.ConnError as exc:
        show_unknown('Could not connect',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    except aws.ClientErr as exc:
        show_unknown('Error retrieving info. Check credentials.',
                     details=dict(error=str(exc).replace(':', '')))
        return False
    if not vpcs:
        show_close('Not VPCs found')
        return False

    result = False

    for vpc in vpcs:
        flow_logs = aws.run_boto3_func(key_id, secret, 'ec2',
                                       'describe_flow_logs',
                                       param='FlowLogs',
                                       retry=retry,
                                       Filters=[{'Name': 'resource-id',
                                                 'Values':
                                                 [vpc['VpcId']]}])
        if not flow_logs:
            show_open('No Flow Logs found for VPC',
                      details=dict(vpc=vpc['VpcId']))
            result = True
        else:
            show_close('Flow Logs found for VPC',
                       details=dict(vpc=vpc['VpcId'],
                                    flow_logs=flow_logs))
    return result
