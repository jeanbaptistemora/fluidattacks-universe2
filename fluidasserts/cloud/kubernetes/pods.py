# -*- coding: utf-8 -*-
"""Kubernetes cloud checks pods."""

# standard imports
from urllib3.exceptions import MaxRetryError

# local imports
from fluidasserts import DAST, MEDIUM, LOW
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
    Check if Pod Security Policies allow pods to run in privileged mode.

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


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def write_root_file_system(*,
                           host: str = None,
                           api_key: str = None,
                           username: str = None,
                           password: str = None,
                           **kwargs):
    """
    Check if Pod Security Policies allow writing to the root file system.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod security policies that allow writing
                to the root file system.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Pod Security Policies allow writing to the root file system.'
    msg_closed: str = \
        'Pod Security Policies do not allow writing to the root file system.'
    vulns, safes = [], []

    pod_security_policies = _get_pod_security_policies(host, api_key, username,
                                                       password, **kwargs)

    for policy in pod_security_policies.items:
        (vulns if not policy.spec.read_only_root_filesystem else safes).append(
            (policy.metadata.self_link,
             'allow pods to write to the root file system.'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def privilege_escalation(*,
                         host: str = None,
                         api_key: str = None,
                         username: str = None,
                         password: str = None,
                         **kwargs):
    """
    Check if Pod Security Policies allow privilege escalation.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod security policies that allow
                privilege escalation.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod Security Policies allow privilege escalation.'
    msg_closed: str = \
        'Pod Security Policies do not allow privilege escalation.'
    vulns, safes = [], []

    pod_security_policies = _get_pod_security_policies(host, api_key, username,
                                                       password, **kwargs)

    for policy in pod_security_policies.items:
        privilege = policy.spec.allow_privilege_escalation
        (vulns if privilege or privilege is None else safes).append(
            (policy.metadata.self_link, 'allow privilege escalation.'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def run_containers_as_root_user(*,
                                host: str = None,
                                api_key: str = None,
                                username: str = None,
                                password: str = None,
                                **kwargs):
    """
    Check if pod security policies allow containers to run as root user.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod security policies that allow
                containers to run as root.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Pod Security Policies that allow containers to run as root.'
    msg_closed: str = \
        'Pod Security Policies that do not allow containers to run as root.'
    vulns, safes = [], []

    pod_security_policies = _get_pod_security_policies(host, api_key, username,
                                                       password, **kwargs)

    for policy in pod_security_policies.items:
        if policy.spec.run_as_user.ranges:
            vulnerable = any(
                list(
                    map(lambda r: 0 in range(r.min, r.max + 1),
                        policy.spec.run_as_user.ranges)))
        else:
            vulnerable = policy.spec.run_as_user.rule != 'MustRunAsNonRoot'

        (vulns if vulnerable else safes).append(
            (policy.metadata.self_link,
             'allow containers to run as root.'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_no_memory_usage_limits(*,
                               host: str = None,
                               api_key: str = None,
                               username: str = None,
                               password: str = None,
                               **kwargs):
    """
    Check if the pod containers do not have a memory usage limit.

    Enforcing memory limits prevents DOS via resource exhaustion.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pods that do not have a memory usage
                 limits.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pods do not set memory usage limits.'
    msg_closed: str = 'Pods set a memory usage limit.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for container in pod.spec.containers:
            limits = container.resources.limits
            (vulns if not limits or not limits.get('memory', None) else
             safes).append((f'{pod.metadata.self_link}',
                            'Must set memory usage limits'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
