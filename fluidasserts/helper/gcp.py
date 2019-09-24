# -*- coding: utf-8 -*-

"""Google Cloud Platform helper."""

# standard imports
import functools
import time

# 3rd party imports
from typing import Any, Callable
from google.oauth2 import service_account
import googleapiclient.discovery


# local imports
# None


class ConnError(ConnectionRefusedError):
    """
    A connection error occurred.

    :py:exc:`ConnectionError` wrapper exception.
    """


def retry_on_errors(func: Callable) -> Callable:
    """Decorate function to retry if a ConnError/ClientErr is raised."""
    @functools.wraps(func)
    def decorated(*args, **kwargs) -> Any:  # noqa
        """Retry the function if a ConnError/ClientErr is raised."""
        if kwargs.get('retry'):
            for _ in range(12):
                try:
                    return func(*args, **kwargs)
                except ConnError:
                    # Wait some seconds and retry
                    time.sleep(5.0)
        return func(*args, **kwargs)
    return decorated


# pylint: disable=unused-argument
# pylint: disable=no-member
@retry_on_errors
def get_iam_policy(
        project_id: str, credentials_file: str,
        retry: bool = True) -> object:
    """
    Get GCP IAM Policy.

    :param project_id: GCP Project Id
    :param credentials_file: JSON file with GCP credentials
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=credentials_file,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'cloudresourcemanager', 'v1', credentials=credentials)

    iam_policy = service.projects().getIamPolicy(resource=project_id, body={})
    resp = iam_policy.execute()
    return resp['bindings']


# pylint: disable=unused-argument
# pylint: disable=no-member
@retry_on_errors
def get_service_accounts(
        project_id: str, credentials_file: str,
        retry: bool = True) -> object:
    """
    Get GCP service accounts.

    :param project_id: GCP Project Id
    :param credentials_file: JSON file with GCP credentials
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=credentials_file,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    name = f'projects/{project_id}'
    serv_acct = service.projects().serviceAccounts().list(name=name)
    resp = serv_acct.execute()
    return [x['name'] for x in resp['accounts']]


# pylint: disable=unused-argument
# pylint: disable=no-member
@retry_on_errors
def get_keys_managed_by_user(
        user: str, credentials_file: str,
        retry: bool = True) -> object:
    """
    Get GCP service accounts.

    :param project_id: GCP Project Id
    :param credentials_file: JSON file with GCP credentials
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=credentials_file,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service = service.projects()
    user_keys = service.serviceAccounts().keys().list(name=user,
                                                      keyTypes='USER_MANAGED')
    resp = user_keys.execute()
    return resp['keys'] if resp else {}
