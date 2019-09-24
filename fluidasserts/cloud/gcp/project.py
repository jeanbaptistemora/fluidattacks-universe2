# -*- coding: utf-8 -*-

"""Google Cloud Platform checks (Project)."""

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
def has_gmail_users(project_id: str, cred_file: str,
                    retry: bool = True) -> tuple:
    """
    Check that corporate login credentials are used instead of Gmail accounts.

    :param project_id: GCP Project Id
    :param cred_file: JSON file with GCP credentials
    """
    roles = gcp.get_iam_policy(project_id=project_id,
                               credentials_file=cred_file, retry=retry)

    msg_open: str = 'Gmail users are present'
    msg_closed: str = 'Not Gmail users are present'

    vulns, safes = [], []
    gmail = []

    if roles:
        gmail = [user for role in roles for user in role['members']
                 if '@gmail.com' in user]

    (vulns if gmail else safes).append(
        (','.join(gmail), 'Must not be present'))

    return _get_result_as_tuple(
        service='Projects', objects='projects',
        msg_open=msg_open, msg_closed=msg_closed,
        vulns=vulns, safes=safes)
