# -*- coding: utf-8 -*-

"""Google Cloud Platform checks (IAM)."""

# standard imports
import json

# 3rd party imports
# None

# local imports
from fluidasserts import DAST, LOW
from fluidasserts.helper import gcp
from fluidasserts.cloud.gcp import _get_result_as_tuple
from fluidasserts.utils.decorators import api, unknown_if


@api(risk=LOW, kind=DAST)
@unknown_if(ConnectionRefusedError, json.decoder.JSONDecodeError)
def has_user_managed_account_keys(project_id: str, cred_file: str,
                                  retry: bool = True) -> tuple:
    """
    Check that services accounts have only GCP-managed account keys.

    :param project_id: GCP Project Id
    :param cred_file: JSON file with GCP credentials
    """
    serv_accounts = gcp.get_service_accounts(project_id=project_id,
                                             credentials_file=cred_file,
                                             retry=retry)

    msg_open: str = 'User managed services keys have user managed keys'
    msg_closed: str = \
        'User managed services keys does not have user managed keys'

    vulns, safes = [], []
    mngd_keys = []

    for user in serv_accounts:
        user_managed_keys = \
            gcp.get_keys_managed_by_user(user,
                                         credentials_file=cred_file,
                                         retry=retry)
        if user_managed_keys:
            mngd_keys.extend([x['name'] for x in user_managed_keys])

    if mngd_keys:
        vulns.append(
            (",".join(mngd_keys),
             'Must not be managing service keys'))

    return _get_result_as_tuple(
        service='Projects', objects='projects',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
