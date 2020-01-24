# -*- coding: utf-8 -*-

"""Fluid Asserts SQL Server package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.sql import SqlManagementClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import _get_result_as_tuple, _get_credentials


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_advanced_data_security_disabled(client_id: str, secret: str,
                                        tenant: str,
                                        subscription_id: str) -> Tuple:
    """
    Check if Advanced Data Security is enabled for SQL Servers.

    Enabling Advanced Data Security on all SQL Servers ensures that SQL server
    data is encrypted and monitored for unusual activity, vulnerabilities, and
    threats.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if Advanced Data Security is disabled for SQL Servers.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Advanced Data Security is disabled for SQL Servers.'
    msg_closed: str = 'Advanced Data Security is enabled for SQL Servers.'

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split('/')[4]
        server_name = serve.id.split('/')[-1]
        policies = list(
            client.server_security_alert_policies.list_by_server(
                group_name, server_name))
        vulnerable = any(list(map(lambda x: x.state == 'Disabled', policies)))
        (vulns if vulnerable else safes).append(
            (serve.id, 'enabled advance security features.'))

    return _get_result_as_tuple(
        objects='Sql Servers',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_ad_administration_disabled(client_id: str,
                                   secret: str,
                                   tenant: str,
                                   subscription_id: str) -> Tuple:
    """
    Check if Active Directory admin is enabled on all SQL servers.

    Enabling Active Directory admin allows users to manage account admins in a
    central location, allowing key rotation and permission management to be
    managed in one location for all servers and databases.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if the Active Directory admin is disabled on any SQL
                 servers.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Active Directory admin is disabled on any SQL servers.'
    msg_closed: str = 'Active Directory admin is enabled on all SQL servers'

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split('/')[4]
        server_name = serve.id.split('/')[-1]
        admins = list(client.server_azure_ad_administrators.list_by_server(
            group_name, server_name))
        vulnerable = not any(list(
            map(lambda x: x.administrator_type == 'ActiveDirectory', admins)))
        (vulns if vulnerable else safes).append(
            (serve.id, 'enable Active Directory admin.'))

    return _get_result_as_tuple(
        objects='Sql Servers',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
