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
from azure.keyvault.secrets import SecretClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import (
    _get_result_as_tuple, _get_credentials, _attr_checker)


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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError, KeyVaultErrorException)
def entities_have_all_access(client_id: str, secret: str, tenant: str,
                             subscription_id: str) -> Tuple:
    """
    Check if users, groups and applications can perform all management actions.

    Grant access to users, groups and applications in a specific area in order
    to preserve the principle of least privilege.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` If there are users, groups and applications that can
                perform all management actions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Users, groups and applications can perform all management actions.'
    msg_closed: str = ('Users, groups and applications can not perform all'
                       ' management actions.')
    vulns, safes = [], []

    rules = {'certificates': lambda x: len(x) == 16,
             'keys': lambda x: len(x) == 16,
             'secrets': lambda x: len(x) == 8}

    credentials = _get_credentials(client_id, secret, tenant)

    key_vault_client = KeyVaultManagementClient(credentials, subscription_id)
    key_vaults = key_vault_client.vaults.list()

    for vault in key_vaults:
        group_name = vault.id.split('/')[4]
        vault = key_vault_client.vaults.get(group_name, vault.name)
        vulnerable = []

        for policy in vault.properties.access_policies:
            vulnerable.append(any(_attr_checker(policy.permissions, rules)))

        (vulns if any(vulnerable) else safes).append(
            (vault.id, 'allow only the required actions.'))

    return _get_result_as_tuple(
        objects='Key Vaults',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError, KeyVaultErrorException)
def has_secret_expiration_disabled(client_id: str, secret: str, tenant: str,
                                   subscription_id: str) -> Tuple:
    """
    Check if the secrets in Azure Key Vault do not have an expiration time set.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are secrets that do not have a set expiration
                time.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'The Secrets in Azure Key Vault do not have an expiry time set.'
    msg_closed: str = 'The Secrets in Azure Key Vault have an expiry time set.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)

    key_vaults = KeyVaultManagementClient(credentials,
                                          subscription_id).vaults.list()
    credentials_ = ClientSecretCredential(
        client_id=client_id, client_secret=secret, tenant_id=tenant)

    for vault in key_vaults:
        key_client = SecretClient(
            vault_url=f'https://{vault.name}.vault.azure.net/',
            credential=credentials_)
        secrets = key_client.list_properties_of_secrets()

        with suppress(KeyVaultManagementClient):
            for secret_ in secrets:
                (vulns if not secret_.expires_on else safes).append(
                    (f'/{secret_.id}', 'set an expiration time.'))

    return _get_result_as_tuple(
        objects='Secrets',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
