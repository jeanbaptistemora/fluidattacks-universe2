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
def get_project_service(
        function: str, project_id: str, credentials_file: str,
        retry: bool = True) -> object:
    """
    Get GCP service object.

    :param function: GCP Service Function
    :param project_id: GCP Project Id
    :param credentials_file: JSON file with GCP credentials
    """
    credentials = service_account.Credentials.from_service_account_file(
        filename=credentials_file,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'cloudresourcemanager', 'v1', credentials=credentials)

    projects = service.projects()
    service_to_call = getattr(projects, function)
    resp = service_to_call(resource=project_id, body={}).execute()
    return resp['bindings']
