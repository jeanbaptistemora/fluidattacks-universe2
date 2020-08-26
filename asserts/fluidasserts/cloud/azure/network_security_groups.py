# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Active directory package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.network import NetworkManagementClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import (_get_result_as_tuple, _get_credentials,
                                      _attr_checker, _port_in_range, _flatten)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def allow_all_ingress_traffic(client_id: str,
                              secret: str,
                              tenant: str,
                              subscription_id: str) -> Tuple:
    """
    Check if Network security groups allow all inbound traffic.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if the there are network security groups that allow
                all inbound traffic.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network security group allow all inbound traffic.'
    msg_closed: str = 'Network security group do no allow all inbound traffic.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    network = NetworkManagementClient(credentials, subscription_id)
    security_groups = network.network_security_groups.list_all()

    rules = {
        'provisioning_state': ['Succeeded'],
        'source_address_prefix': ['*']
    }

    for group in security_groups:
        allow_rules = list(
            filter(lambda r: r.access == 'Allow' and r.direction == 'Inbound',
                   group.security_rules))
        vulnerable = any([all(_attr_checker(i, rules)) for i in allow_rules])
        (vulns if vulnerable else safes).append((group.id, 'Message'))

    return _get_result_as_tuple(
        objects='Network security groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_open_all_ports_to_the_public(client_id: str, secret: str, tenant: str,
                                     subscription_id: str) -> Tuple:
    """
    Check if security groups has all ports or protocols open to the public.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are network security groups that has all
                ports open to the all public.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network security groups has all ports open to the pubic.'
    msg_closed: str = \
        'Network security groups do not has all ports open to the pubic.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    network = NetworkManagementClient(credentials, subscription_id)
    security_groups = network.network_security_groups.list_all()

    rules = {
        'destination_port_range': ['*', '0-65535'],
        'source_address_prefix': ['*'],
        'provisioning_state': ['Succeeded'],
        'protocol': ['*']
    }

    for group in security_groups:
        allow_rules = list(
            filter(lambda r: r.access == 'Allow' and r.direction == 'Inbound',
                   group.security_rules))
        vulnerable = any([all(_attr_checker(i, rules)) for i in allow_rules])
        (vulns if vulnerable else safes).append(
            (group.id, 'do not open all ports to the public.'))

    return _get_result_as_tuple(
        objects='Network security groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_admin_ports_open_to_the_public(client_id: str, secret: str,
                                       tenant: str,
                                       subscription_id: str) -> Tuple:
    """
    Check if security groups has all ports or protocols open to the public.

    Admin Ports.
        - 20        ``FTP``.
        - 21        ``FTP``.
        - 22        ``SSH``.
        - 53        ``DNS``.
        - 445       ``CIFS``.
        - 1521      ``Oracle``.
        - 2438      ``Oracle``.
        - 3306      ``MySQL``.
        - 3389      ``RDP``.
        - 5432      ``Postgres``.
        - 6379      ``Redis``.
        - 7199      ``Cassandra``.
        - 8111      ``DAX``.
        - 8888      ``Cassandra``.
        - 9160      ``Cassandra``.
        - 11211     ``Memcached``.
        - 27017     ``Mongo DB``.
        - 445       ``CIFS``.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are network security groups that has all
                ports open to the all public.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    admin_ports = {
        20,  # FTP
        21,  # FTP
        22,  # SSH
        53,  # DNS
        445,  # CIFS
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
        445,  # CIFS
    }
    msg_open: str = \
        'Network security groups allow the public access to admin_ports.'
    msg_closed: str = ('Network security groups do not allow the'
                       ' public access to admin_ports.')
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    network = NetworkManagementClient(credentials, subscription_id)
    security_groups = network.network_security_groups.list_all()
    rules = {
        'source_address_prefix': ['*'],
        'provisioning_state': ['Succeeded'],
        'access': 'Allow',
        'direction': 'Inbound'
    }
    for group in security_groups:
        allow_rules = list(
            filter(lambda r: _attr_checker(r, rules), group.security_rules))
        vulnerable = _flatten(list(
            map(lambda rul: list(
                map(lambda port:
                    _port_in_range(port,
                                   _flatten(
                                       [rul.destination_port_range,
                                        rul.destination_port_ranges])),
                    admin_ports)), allow_rules)))

        (vulns if any(vulnerable) else safes).append(
            (group.id, 'do not allow public access to any admin_port.'))

    return _get_result_as_tuple(
        objects='Network security groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_insecure_port_ranges(client_id: str,
                             secret: str,
                             tenant: str,
                             subscription_id: str) -> Tuple:
    """
    Check if security groups implement range of ports to allow inbound traffic.

    Establishing a range of ports within security groups is not a good
    practice, because attackers can use port scanners to identify what services
    are running in instances.

    :param key_id: AWS Key Id.
    :param secret: AWS Key Secret.

    :returns: - ``OPEN`` if the there are network security groups that
                implements a range of ports.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network security groups have port ranges established.'
    msg_closed: str = \
        'Network security groups do not have port ranges established.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    network = NetworkManagementClient(credentials, subscription_id)
    security_groups = network.network_security_groups.list_all()
    rules = {
        'destination_port_range': lambda x: len(x) > 1,
        'destination_port_ranges': lambda x: any([i in x for i in ['*', '-']])
    }
    for group in security_groups:
        allow_rules = list(
            filter(lambda r: r.access == 'Allow' and r.direction == 'Inbound',
                   group.security_rules))
        vulnerable = any([any(_attr_checker(i, rules)) for i in allow_rules])
        (vulns if vulnerable else safes).append(
            (group.id, 'should not implement a range of ports.'))

    return _get_result_as_tuple(
        objects='Network security groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_flow_logs_disabled(client_id: str, secret: str, tenant: str,
                           subscription_id: str) -> Tuple:
    """
    Check if Network security groups has flow logs disabled.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are network security groups that
                has flow logs disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network security groups has flow logs disabled.'
    msg_closed: str = 'Network security groups has flow logs enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    network = NetworkManagementClient(credentials, subscription_id)
    security_groups = network.network_security_groups.list_all()
    for group in security_groups:
        flow_status = network.network_watchers.get_flow_log_status(
            resource_group_name='NetworkWatcherRG',
            network_watcher_name='NetworkWatcher_eastus',
            target_resource_id=group.id).result()

        (vulns if not flow_status.enabled else safes).append(
            (group.id, 'must enable flow logs.'))

    return _get_result_as_tuple(
        objects='Network security groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
