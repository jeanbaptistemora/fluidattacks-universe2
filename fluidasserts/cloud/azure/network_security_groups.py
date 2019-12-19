# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Active directory package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException
from azure.mgmt.network import NetworkManagementClient

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import (
    _get_result_as_tuple, _get_credentials, _attr_checker)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException, AuthenticationError)
def allow_all_ingress_traffic(client_id: str,
                              secret: str,
                              tenant: str,
                              subscription_id: str) -> Tuple:
    """
    Check if Network security groups allow all inbound traffic.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.
    :param subscription_id: Azure subscription ID.

    :returns: - ``OPEN`` if the there are network security groups that allow
                all inbound traffic.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Network security group allow all inbound traffic.'
    msg_closed: str = 'Network security group do no allow all inbound traffic.'
    vulns, safes = [], []

    credentials = _get_credentials(client_id, secret, tenant)
    network = NetworkManagementClient(credentials, subscription_id)
    security_groups = network.network_security_groups.list_all()

    rules = {
        'provisioning_state': ['Succeeded'],
        'source_address_prefix': ['*']
    }

    for group in security_groups:
        allow_rules = list(
            filter(lambda r: r.access == 'Allow' and r.direction == 'Inbound',
                   group.security_rules))
        vulnerable = any([all(_attr_checker(i, rules)) for i in allow_rules])
        (vulns if vulnerable else safes).append((group.id, 'Message'))

    return _get_result_as_tuple(
        objects='Network security groups',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
