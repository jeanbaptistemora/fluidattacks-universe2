# -*- coding: utf-8 -*-

"""Fluid Asserts App Services package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.web import WebSiteManagementClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import _get_result_as_tuple, _get_credentials


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_authentication_disabled(client_id: str,
                                secret: str,
                                tenant: str,
                                subscription_id: str) -> Tuple:
    """
    Check if the Authentication is disabled for App Services.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are App Services that not have Authentication
                 enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Application services do not have authentication enabled.'
    msg_closed: str = 'Application services have authentication enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    webapps = WebSiteManagementClient(credentials, subscription_id).web_apps

    for web in webapps.list():
        group_name = web.id.split('/')[4]
        auth_settings = webapps.get_auth_settings(group_name, web.name)
        (vulns if not auth_settings.enabled else safes).append(
            (web.id, 'enable App Service Authentication.'))

    return _get_result_as_tuple(
        objects='App Services',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_client_certificates_disabled(client_id: str, secret: str, tenant: str,
                                     subscription_id: str) -> Tuple:
    """
    Check if the client certificates are disabled for App Services.

    Enabling Client Certificates will block all clients that do not have a
    valid certificate from accessing the app.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are App Services that not have client
                 certificates enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Application services do not have client certificates enabled.'
    msg_closed: str = 'Application services have client certificates enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    webapps = WebSiteManagementClient(credentials, subscription_id).web_apps

    for web in webapps.list():
        (vulns if not web.client_cert_enabled else safes).append(
            (web.id, 'enable App Service client certificates.'))

    return _get_result_as_tuple(
        objects='App Services',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_https_only_disabled(client_id: str, secret: str, tenant: str,
                            subscription_id: str) -> Tuple:
    """
    Check if HTTPS only is disabled for App Services.

    Enabling HTTPS Only traffic will redirect all non-secure HTTP requests to
    HTTPS. HTTPS uses the SSL/TLS protocol to provide a secure connection.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are App Services that not have HTTPS only
                 enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Application services do not have HTTPS only enabled.'
    msg_closed: str = 'Application services have HTTPS only enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    webapps = WebSiteManagementClient(credentials, subscription_id).web_apps

    for web in webapps.list():
        (vulns if not web.https_only else safes).append(
            (web.id, 'enable HTTPS only.'))

    return _get_result_as_tuple(
        objects='App Services',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_identity_disabled(client_id: str, secret: str, tenant: str,
                          subscription_id: str) -> Tuple:
    """
    Check if managed identity is disabled for App Services.

    Managed identities for Azure resources provides Azure services with a
    managed identity in Azure AD which can be used to authenticate to any
    service that supports Azure AD authentication, without having to include
    any credentials in code.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if there are App Services that not have managed
                 identity enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Application services do not have managed identity enabled.'
    msg_closed: str = 'Application services have managed identity enabled.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    webapps = WebSiteManagementClient(credentials, subscription_id).web_apps

    for web in webapps.list():
        (vulns if not web.identity else safes).append(
            (web.id, 'enable managed identity for App Services.'))

    return _get_result_as_tuple(
        objects='App Services',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
