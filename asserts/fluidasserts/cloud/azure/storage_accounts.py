# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Storage Accounts package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.storage import StorageManagementClient
from azure.storage.file import FileService

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import _get_result_as_tuple, _get_credentials


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def use_microsoft_managed_keys(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
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
    msg_open: str = (
        "Storage accounts use keys managed by Microsoft for encryption."
    )
    msg_closed: str = (
        "Storage accounts use client-managed keys for encryption."
    )
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage_accounts = StorageManagementClient(
        credentials, subscription_id
    ).storage_accounts.list()
    for account in storage_accounts:
        (
            vulns if not account.encryption.key_vault_properties else safes
        ).append((account.id, "use client-managed keys for encryption."))

    return _get_result_as_tuple(
        objects="Storage accounts",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_insecure_transport(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if Storage account endpoints allow use HTTP.

    Storage Accounts can contain sensitive information and should only be
    accessed over HTTPS. Enabling the HTTPS-only flag ensures that Azure does
    not allow HTTP traffic to Storage Accounts.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are Storage Accounts that do not use
                HTTP-only.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Storage account endpoints do not use HTTPS-only."
    msg_closed: str = "Storage account endpoints use HTTPS-only."
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage_accounts = StorageManagementClient(
        credentials, subscription_id
    ).storage_accounts.list()
    for account in storage_accounts:
        (vulns if not account.enable_https_traffic_only else safes).append(
            (account.id, "only HTTPS should be allowed.")
        )

    return _get_result_as_tuple(
        objects="Storage accounts.",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def blob_containers_are_public(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if Blob containers are publicly accessible.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are blob containers publicly accessible.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Blob containres are publicly accessible."
    msg_closed: str = "Blob containers are private."
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage = StorageManagementClient(credentials, subscription_id)
    storage_accounts = storage.storage_accounts.list()
    for account in storage_accounts:
        group_name = account.id.split("/")[4]
        blob_containers = storage.blob_containers.list(
            group_name, account.name
        )
        for container in blob_containers:
            (vulns if container.public_access != "None" else safes).append(
                (container.id, "does not allow public access to containers.")
            )

    return _get_result_as_tuple(
        objects="Storage accounts",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def allow_access_from_all_networks(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if Storage accounts allow access from all networks.

    Ensures that Storage Account access is restricted to trusted networks.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are storage accounts that allow access from
                all networks.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Storage accounts allow access from all networks."
    msg_closed: str = (
        "Storage accounts restrict access only to trusted networks."
    )
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage_accounts = StorageManagementClient(
        credentials, subscription_id
    ).storage_accounts.list()
    for account in storage_accounts:
        (
            vulns
            if account.network_rule_set.default_action == "Allow"
            else safes
        ).append((account.id, "allow access only to trusted networks."))
    return _get_result_as_tuple(
        objects="Storage accounts",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def file_shares_has_global_acl_permissions(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if File Shares allow full write, delete, or read ACL permissions.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are File Shares that allow global ACL
                permissions.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = (
        "File Shares allow full write, delete, or read ACL permissions."
    )
    msg_closed: str = "File Shares do not allow global ACL permissions."
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage = StorageManagementClient(credentials, subscription_id)
    storage_accounts = storage.storage_accounts

    for account in storage_accounts.list():
        group_name = account.id.split("/")[4]
        keys = storage_accounts.list_keys(group_name, account.name)

        file_service = FileService(
            account_name=account.name, account_key=keys.keys[0].value
        )
        for shared in file_service.list_shares().items:
            acls: dict = file_service.get_share_acl(share_name=shared.name)
            success = any(
                list(map(lambda acl: len(acl.permission) == 5, acls.values()))
            )
            (vulns if success else safes).append(
                (
                    f"/{account.primary_endpoints.file}{shared.name}",
                    "do not allow global ACL permissions.",
                )
            )

    return _get_result_as_tuple(
        objects="File shares",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def file_shares_acl_permissions_do_not_expire(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if the ACL permissions of the File shares do not expire.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are ACL permissions that do not expire.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "The ACL permissions of the File Shares do not expire."
    msg_closed: str = "The ACL permissions of the File Shares expire."
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage = StorageManagementClient(credentials, subscription_id)
    storage_accounts = storage.storage_accounts

    for account in storage_accounts.list():
        group_name = account.id.split("/")[4]
        keys = storage_accounts.list_keys(group_name, account.name)

        file_service = FileService(
            account_name=account.name, account_key=keys.keys[0].value
        )
        for shared in file_service.list_shares().items:
            acls: dict = file_service.get_share_acl(share_name=shared.name)
            success = any(
                list(map(lambda acl: acl.expiry is None, acls.values()))
            )
            (vulns if success else safes).append(
                (
                    f"/{account.primary_endpoints.file}{shared.name}",
                    "set an expiration time.",
                )
            )

    return _get_result_as_tuple(
        objects="File shares",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_blob_container_mutability(
    client_id: str, secret: str, tenant: str, subscription_id: str
) -> Tuple:
    """
    Check if blob containers do not have an immutability policy.

    Immutable storage helps store data securely by protecting critical data
    against deletion.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are blob containers that do not have an
                 immutability policy.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = "Blob containers do not have an immutability policy."
    msg_closed: str = "Blob containers have an immutability policy."
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    storage = StorageManagementClient(credentials, subscription_id)
    storage_accounts = storage.storage_accounts.list()
    for account in storage_accounts:
        group_name = account.id.split("/")[4]
        blob_containers = storage.blob_containers.list(
            group_name, account.name
        )
        for container in blob_containers:
            (vulns if not container.has_immutability_policy else safes).append(
                (container.id, "enable a data immutability policy.")
            )

    return _get_result_as_tuple(
        objects="Storage accounts",
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes,
    )
