# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Storage Accounts package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.storage import StorageManagementClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import (_get_result_as_tuple, _get_credentials)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def use_microsoft_managed_keys(client_id: str, secret: str, tenant: str,
                               subscription_id: str) -> Tuple:
    """
    Check if Storage Accounts use keys managed by Microsoft for encryption.

    Use client-managed keys for encryption of Storage Accounts.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are Storage Accounts that use keys
                managed by Microsoft for encryption..
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Storage accounts use keys managed by Microsoft for encryption.'
    msg_closed: str = \
        'Storage accounts use client-managed keys for encryption.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage_accounts = StorageManagementClient(
        credentials, subscription_id).storage_accounts.list()
    for account in storage_accounts:
        (vulns
         if not account.encryption.key_vault_properties else safes).append(
             (account.id, 'use client-managed keys for encryption.'))

    return _get_result_as_tuple(
        objects='Storage accounts',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
