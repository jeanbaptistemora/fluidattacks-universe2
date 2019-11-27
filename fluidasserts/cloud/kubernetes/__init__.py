# -*- coding: utf-8 -*-
"""Fluid Asserts Kubernetes package."""

# standard imports
from typing import List
from urllib3.exceptions import MaxRetryError

# 3rd party imports
from kubernetes import client
from kubernetes.client import Configuration  # noqa
from kubernetes.client.rest import ApiException

# local imports
from fluidasserts import Unit, OPEN, CLOSED


def _get_result_as_tuple(*, host: str, objects: str, msg_open: str,
                         msg_closed: str, vulns: List[str],
                         safes: List[str]) -> tuple:
    """Return the tuple version of the Result object."""
    if host.endswith('/'):
        host = host[:-1]
    vuln_units: List[Unit] = []
    safe_units: List[Unit] = []

    if vulns:
        vuln_units.extend(
            Unit(where=f'{host}{url_}', specific=[vuln])
            for url_, vuln in vulns)
    if safes:
        safe_units.extend(
            Unit(where=f'{host}{url_}', specific=[safe])
            for url_, safe in safes)

    if vulns:
        return OPEN, msg_open, vuln_units, safe_units
    if safes:
        return CLOSED, msg_closed, vuln_units, safe_units
    return CLOSED, f'No {objects} found to check', vuln_units, safe_units


def _get_config(host: str = None,
                api_key: str = None,
                username: str = None,
                password: str = None,
                **kwargs):
    """
    Configure connection to the Kubernetes API server.

    Can use API Key or Username and Password.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :rtype: :class:`kubernetes.client.Configuration`
    """
    configuration = Configuration()
    configuration.host = host
    configuration.username = username
    configuration.password = password
    configuration.api_key['authorization'] = api_key
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.verify_ssl = False

    for key, value in kwargs.items():
        setattr(configuration, key, value)

    return configuration


def _get_api_instance(api: str,
                      host: str = None,
                      api_key: str = None,
                      username: str = None,
                      password: str = None,
                      **kwargs):
    """
    Create an instance of the api version provided to make requests.

    Can use API Key or Username and Password.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.
    """
    api_to_call = getattr(client, api)
    return api_to_call(client.ApiClient(_get_config(
        host, api_key, username, password, **kwargs)))


def run_function(api_instance: object,
                 func: str,
                 **kwargs):
    """
    Run the function provided for the API instance provided.

    :param api_instance: API version instance.
    :param func: API method to call.
    """
    method_to_call = getattr(api_instance, func)
    try:
        return method_to_call(_request_timeout=5, **kwargs)
    except (ApiException, MaxRetryError) as exc:
        raise exc
