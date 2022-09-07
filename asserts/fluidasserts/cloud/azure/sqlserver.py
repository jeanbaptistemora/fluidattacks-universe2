# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Fluid Asserts SQL Server package."""


from azure.mgmt.sql import (
    SqlManagementClient,
)
from fluidasserts import (
    DAST,
    MEDIUM,
)
from fluidasserts.cloud.azure import (
    _get_credentials,
    _get_result_as_tuple,
)
from fluidasserts.utils.decorators import (
    api,
    unknown_if,
)
from msrest.exceptions import (
    AuthenticationError,
    ClientException,
)
from typing import (
    Tuple,
)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_advanced_data_security_disabled(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
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
    msg_open: str = "Advanced Data Security is disabled for SQL Servers."
    msg_closed: str = "Advanced Data Security is enabled for SQL Servers."

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split("/")[4]
        server_name = serve.id.split("/")[-1]
        policies = list(
            client.server_security_alert_policies.list_by_server(
                group_name, server_name
            )
        )
        vulnerable = any(list(map(lambda x: x.state == "Disabled", policies)))
        (vulns if vulnerable else safes).append(
            (serve.id, "enabled advance security features.")
        )

    return _get_result_as_tuple(
        objects="Sql Servers",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_ad_administration_disabled(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
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
    msg_open: str = "Active Directory admin is disabled on any SQL servers."
    msg_closed: str = "Active Directory admin is enabled on all SQL servers"

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split("/")[4]
        server_name = serve.id.split("/")[-1]
        admins = list(
            client.server_azure_ad_administrators.list_by_server(
                group_name, server_name
            )
        )
        vulnerable = not any(
            list(
                map(
                    lambda x: x.administrator_type == "ActiveDirectory", admins
                )
            )
        )
        (vulns if vulnerable else safes).append(
            (serve.id, "enable Active Directory admin.")
        )

    return _get_result_as_tuple(
        objects="Sql Servers",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def allow_public_access(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if SQL Servers are publicly accessible.

    Unless there is a specific business requirement, SQL Server instances
    should not have a public endpoint.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are SQL servers publicly accessible.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "SQL Servers are publicly accessible."
    msg_closed: str = "SQL Servers are not publicly accessible."

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split("/")[4]
        server_name = serve.id.split("/")[-1]
        rules = list(
            client.firewall_rules.list_by_server(group_name, server_name)
        )
        vulnerable = any(
            list(
                map(
                    lambda x: "0.0.0.0"
                    in [x.end_ip_address, x.start_ip_address],  # nosec
                    rules,
                )
            )
        )
        (vulns if vulnerable else safes).append(
            (serve.id, "do not allow public access.")
        )

    return _get_result_as_tuple(
        objects="Sql Servers",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_transparent_encryption_disabled(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if SQL Server has transparent encryption disabled.

    Transparent data encryption encrypts your databases, backups, and logs at
    rest without any changes to your application.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are SQL servers that have transparent
                 encryption disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "SQL Servers has transparent encryption disabled."
    msg_closed: str = "SQL Servers has transparent encryption enabled."

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split("/")[4]
        server_name = serve.id.split("/")[-1]
        databases = list(
            client.databases.list_by_server(group_name, server_name)
        )

        for database in databases:
            encryption = client.transparent_data_encryptions.get(
                group_name, server_name, database.name
            )

            (vulns if encryption.status == "Disabled" else safes).append(
                (database.id, "enable transparent encryption.")
            )

    return _get_result_as_tuple(
        objects="Sql Servers",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def use_microsoft_managed_keys(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if SQL servers use Microsoft managed keys for transparent encryption.

    With TDE with Azure Key Vault integration, can control key management
    tasks on all TDE protectors using Azure Key Vault functionality.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are SQL servers that use Microsoft managed
                 keys for transparent encryption.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "SQL servers use Microsoft managed keys for transparent encryption."
    )
    msg_closed: str = (
        "SQL servers use customer managed keys for transparent encryption."
    )

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split("/")[4]
        server_name = serve.id.split("/")[-1]

        protectors = list(
            client.encryption_protectors.list_by_server(
                group_name,
                server_name,
            )
        )
        vulnerable = any(
            list(
                map(
                    lambda x: "ServiceManaged"
                    in [x.server_key_name, x.server_key_type],
                    protectors,
                )
            )
        )

        (vulns if vulnerable else safes).append(
            (serve.id, "use customer managed keys.")
        )

    return _get_result_as_tuple(
        objects="Sql Servers",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_server_auditing_disabled(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if SQL Server Auditing is disabled for SQL servers.

    Enabling SQL Server Auditing ensures that all activities are being logged
    properly, including potentially-malicious activity.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are SQL servers that have auditing disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "SQL Server Auditing is disabled for SQL servers."
    msg_closed: str = "SQL Server Auditing is enabled for SQL servers."

    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    client = SqlManagementClient(credentials, subscription_id)

    for serve in client.servers.list():
        group_name = serve.id.split("/")[4]
        server_name = serve.id.split("/")[-1]
        policies = list(
            client.server_blob_auditing_policies.list_by_server(
                group_name, server_name
            )
        )
        vulnerable = any(list(map(lambda x: x.state == "Disabled", policies)))

        (vulns if vulnerable else safes).append(
            (serve.id, "enable SQL Server Auditing.")
        )

    return _get_result_as_tuple(
        objects="Sql Servers",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
