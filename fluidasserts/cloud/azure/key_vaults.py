# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Key Vaults package."""

# standar imports
from typing import Tuple
from contextlib import suppress

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.keyvault.keys._shared._generated.v7_0.models._models_py3 import (
    KeyVaultErrorException)
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.identity import ClientSecretCredential
from azure.keyvault.keys import KeyClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import (_get_result_as_tuple, _get_credentials)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError, KeyVaultErrorException)
def has_key_expiration_disabled(client_id: str, secret: str, tenant: str,
                                subscription_id: str) -> Tuple:
    """
    Check if the keys in Azure Key Vault do not have an expiration time set.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` If there are keys that do not have a set expiration
                time.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'The Keys in Azure Key Vault do not have an expiry time set.'
    msg_closed: str = 'The Keys in Azure Key Vault have an expiry time set.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)

    key_vaults = KeyVaultManagementClient(credentials,
                                          subscription_id).vaults.list()
    credentials_ = ClientSecretCredential(
        client_id=client_id, client_secret=secret, tenant_id=tenant)

    for vault in key_vaults:
        key_client = KeyClient(
            vault_url=f'https://{vault.name}.vault.azure.net/',
            credential=credentials_)
        keys = key_client.list_properties_of_keys()

        with suppress(KeyVaultManagementClient):
            for key in keys:
                (vulns if not key.expires_on else safes).append(
                    (f'/{key.id}', 'set an expiration time.'))

    return _get_result_as_tuple(
        objects='Keys',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
