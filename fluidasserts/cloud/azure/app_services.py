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
