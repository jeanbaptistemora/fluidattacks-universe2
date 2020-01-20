# -*- coding: utf-8 -*-

"""Fluid Asserts Security Center package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.security import SecurityCenter

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import _get_result_as_tuple, _get_credentials


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def has_admin_security_alerts_disabled(client_id: str,
                                       secret: str,
                                       tenant: str,
                                       subscription_id: str,
                                       region: str = 'east-us') -> Tuple:
    """
    Check if security alerts are not configured to be sent to admins.

    Enabling security alerts to be sent to admins ensures that detected
    vulnerabilities and security issues are sent to the subscription admins for
    quick remediation.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if security alerts are not configured to be sent to
                 admins.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Security alerts are not configured to be sent to admins.'
    msg_closed: str = 'Security alerts are configured to be sent to admins.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    center = SecurityCenter(credentials, subscription_id,
                            region).security_contacts

    (vulns if not list(center.list()) else
     safes).append((f'subscriptions/{subscription_id}',
                    'configure security alerts.'))

    return _get_result_as_tuple(
        objects='Security center',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
