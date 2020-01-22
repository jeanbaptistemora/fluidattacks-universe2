# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Virtual Machines package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.compute import ComputeManagementClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import (_get_result_as_tuple, _get_credentials)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_os_disk_encryption_disabled(client_id: str, secret: str, tenant: str,
                                    subscription_id: str) -> Tuple:
    """
    Check if Virtual Machines OS Disks has encryption disabled.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are OS disk that do not have
                encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'OS disks has encryption disabled.'
    msg_closed: str = 'OS disks has encryption enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)

    disks = ComputeManagementClient(credentials, subscription_id).disks.list()

    for disk in filter(lambda d: d.os_type is not None, disks):
        (vulns if not disk.encryption_settings_collection else safes).append(
            (disk.id, 'must enable encryption.'))

    return _get_result_as_tuple(
        objects='Disks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_data_disk_encryption_disabled(client_id: str, secret: str, tenant: str,
                                      subscription_id: str) -> Tuple:
    """
    Check if Virtual Machines Data Disks has encryption disabled.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are disk that do not have
                encryption enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Data Disks has encryption disabled.'
    msg_closed: str = 'Data Disks has encryption enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)

    disks = ComputeManagementClient(credentials, subscription_id).disks.list()

    for disk in filter(lambda d: d.os_type is None, disks):
        (vulns if not disk.encryption_settings_collection else safes).append(
            (disk.id, 'must enable encryption.'))

    return _get_result_as_tuple(
        objects='Disks',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def have_automatic_updates_disabled(client_id: str, secret: str, tenant: str,
                                    subscription_id: str) -> Tuple:
    """
    Check if Virtual Machines have disabled automatic updates.

    This check only apply for windows machines.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are Virtual Machines that has automatic
                updates disabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Virtual machines have automatic updates disabled.'
    msg_closed: str = 'Virtual machines have automatic updates enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)

    virtual_machines = ComputeManagementClient(
        credentials, subscription_id).virtual_machines.list_all()

    for machine in virtual_machines:
        if machine.os_profile.windows_configuration:
            config = machine.os_profile.windows_configuration
            (vulns if not config.enable_automatic_updates else safes).append(
                (machine.id, 'enable automatic updates.'))

    return _get_result_as_tuple(
        objects='Virtual Machines',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_identity_disabled(client_id: str, secret: str, tenant: str,
                          subscription_id: str) -> Tuple:
    """
    Check if managed identity is disabled for Virtual Machines.

    Managed identities for Azure resources provides Azure services with a
    managed identity in Azure AD which can be used to authenticate to any
    service that supports Azure AD authentication, without having to include
    any credentials in code.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are Virtual Machines that not have managed
                 identity enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Virtual Machines do not have managed identity enabled.'
    msg_closed: str = 'Virtual Machines have managed identity enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    virtual_machines = ComputeManagementClient(
        credentials, subscription_id).virtual_machines.list_all()

    for virtual_m in virtual_machines:
        (vulns if not virtual_m.identity else safes).append(
            (virtual_m.id, 'enable managed identity for Virtual Machines.'))

    return _get_result_as_tuple(
        objects='Virtual Machines.',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
