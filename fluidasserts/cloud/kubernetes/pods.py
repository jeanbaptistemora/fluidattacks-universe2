# -*- coding: utf-8 -*-
"""Kubernetes cloud checks pods."""

# standard imports
from urllib3.exceptions import MaxRetryError

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.kubernetes import _get_result_as_tuple, \
    _get_api_instance, run_function

# 3rd party imports
from kubernetes.client.rest import ApiException  # noqa


def _get_pod_security_policies(host: str = None,
                               api_key: str = None,
                               username: str = None,
                               password: str = None,
                               **kwargs):
    """Get pod policies for all namespaces."""
    api_instance = _get_api_instance('PolicyV1beta1Api',
                                     host, api_key,
                                     username,
                                     password,
                                     **kwargs)
    return run_function(api_instance, 'list_pod_security_policy')


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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def privileged_containers(*,
                          host: str = None,
                          api_key: str = None,
                          username: str = None,
                          password: str = None,
                          **kwargs):
    """
    Check if Pod Security Policies allow pods run in privileged mode.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod security policies that allow pods
                run in privileged mode.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Pod Security Policies allow pods to run in privileged mode.'
    msg_closed: str = \
        'Pod Security Policies do not allow pods to run in privileged mode.'
    vulns, safes = [], []

    pod_security_policies = _get_pod_security_policies(host, api_key, username,
                                                       password, **kwargs)

    for policy in pod_security_policies.items:
        (vulns if policy.spec.privileged else safes).append(
            (policy.metadata.self_link,
             'pods are allowed to run in privileged mode.'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
