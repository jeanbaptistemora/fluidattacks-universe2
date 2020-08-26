# -*- coding: utf-8 -*-

"""Fluid Asserts Azure Active directory package."""

# standar imports
from typing import Tuple

# 3rd party imports
from msrest.exceptions import AuthenticationError, ClientException

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.azure import _get_result_as_tuple, _get_credentials


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ClientException)
def are_valid_credentials(client_id: str,
                          secret: str,
                          tenant: str) -> Tuple:
    """
    Check if given Azure credentials are working.

    :param client_id: Azure service client_id.
    :param secret: Azure service secret.
    :param tenant: Azure service tenant.

    :returns: - ``OPEN`` if the credentials are valid.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    vulns, safes = [], []
    msg_open: str = 'Provided Azure Credentials are valid.'
    msg_closed: str = 'Provided Azure Credentials are not valid.'
    try:
        credentials = _get_credentials(client_id, secret, tenant)
        vulns.append((f"Users/{credentials.id}", 'are valid'))
    except AuthenticationError:
        safes.append((f'Users/{client_id}', 'are invalid.'))

    return _get_result_as_tuple(objects='Users',
                                msg_open=msg_open,
                                msg_closed=msg_closed,
                                vulns=vulns,
                                safes=safes)
