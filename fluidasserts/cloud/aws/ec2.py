# -*- coding: utf-8 -*-

"""
AWS cloud checks (EC2).

The checks are based on CIS AWS Foundations Benchmark.
"""

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
def seggroup_allows_anyone_to_ssh(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if security groups allows connection from anyone to SSH service.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        sec_groups = aws.list_security_groups(key_id, secret, retry=retry)
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
        for ip_perm in group['IpPermissions']:
            try:
                vuln = [ip_perm for x in ip_perm['IpRanges']
                        if x['CidrIp'] == '0.0.0.0/0'and
                        ip_perm['FromPort'] <= 22 <= ip_perm['ToPort']]
            except KeyError:
                pass
        if vuln:
            show_open('Security group allows connections \
from anyone to port 22',
                      details=dict(group=group['Description'],
                                   ip_ranges=vuln))
            result = True
        else:
            show_close('Security group not allows connections \
from anyone to port 22',
                       details=dict(group=group['Description']))
    return result


@notify
@level('medium')
@track
def seggroup_allows_anyone_to_rdp(
        key_id: str, secret: str, retry: bool = True) -> bool:
    """
    Check if security groups allows connection from anyone to RDP service.

    :param key_id: AWS Key Id
    :param secret: AWS Key Secret
    """
    try:
        sec_groups = aws.list_security_groups(key_id, secret, retry=retry)
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
        for ip_perm in group['IpPermissions']:
            try:
                vuln = [ip_perm for x in ip_perm['IpRanges']
                        if x['CidrIp'] == '0.0.0.0/0'and
                        ip_perm['FromPort'] <= 3389 <= ip_perm['ToPort']]
            except KeyError:
                pass
        if vuln:
            show_open('Security group allows connections \
from anyone to port 3389',
                      details=dict(group=group['Description'],
                                   ip_ranges=vuln))
            result = True
        else:
            show_close('Security group not allows connections \
from anyone to port 3389',
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
        sec_groups = aws.list_security_groups(key_id, secret, retry=retry)
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
        volumes = aws.list_volumes(key_id, secret, retry=retry)
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
