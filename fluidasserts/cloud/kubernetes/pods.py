# -*- coding: utf-8 -*-
"""Kubernetes cloud checks pods."""

# standard imports
from urllib3.exceptions import MaxRetryError

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.kubernetes import _get_result_as_tuple, _get_config

# 3rd party imports
from kubernetes.client.rest import ApiException  # noqa
from kubernetes import client  # noqa


def _get_pod_security_policies(host: str = None,
                               api_key: str = None,
                               username: str = None,
                               password: str = None,
                               **kwargs):
    """Get pod policies for all namespaces."""
    api_instance = client.PolicyV1beta1Api(
        client.ApiClient(
            _get_config(host, api_key, username, password, **kwargs)))
    try:
        api_response = api_instance.list_pod_security_policy(
            _request_timeout=5)
    except (ApiException, MaxRetryError) as exc:
        raise exc
    return api_response


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def undefined_pod_security_policies(*,
                                    host: str = None,
                                    api_key: str = None,
                                    username: str = None,
                                    password: str = None,
                                    **kwargs):
    """
    Check if Pod Security Policies are undefined.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pods without security policies.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod Security Policies are undefined.'
    msg_closed: str = 'Pod Security Policies are defined.'
    vulns, safes = [], []

    pod_security_policies = _get_pod_security_policies(host, api_key, username,
                                                       password, **kwargs)

    (vulns if not pod_security_policies.items else safes).append(
        (pod_security_policies.metadata.self_link,
         'Define Pod Security Policies.'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
