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
