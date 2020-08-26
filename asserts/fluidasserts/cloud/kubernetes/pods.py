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


def _check_security_context_attribute(*,
                                      host: str = None,
                                      api_key: str = None,
                                      username: str = None,
                                      password: str = None,
                                      attribute_check: dict = None):
    """Separate containers that compliance the conditions."""
    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password)
    vulns, safes = [], []
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for container in pod.spec.containers:
            context = container.security_context
            for attribute, check in attribute_check.items():
                (vulns
                 if check(getattr(context, attribute)) else safes).append(
                     pod.metadata.self_link)
    return (vulns, safes)


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


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_no_cpu_usage_limits(*,
                            host: str = None,
                            api_key: str = None,
                            username: str = None,
                            password: str = None,
                            **kwargs):
    """
    Check if the pod containers do not have a CPU usage limit.

    Enforcing CPU limits prevents DOS via resource exhaustion.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pods that do not have CPU usage limits.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pods do not set CPU usage limits.'
    msg_closed: str = 'Pods set CPU usage limits.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for container in pod.spec.containers:
            limits = container.resources.limits
            (vulns
             if not limits or not limits.get('cpu', None) else safes).append(
                 (f'{pod.metadata.self_link}', 'Must set CPU usage limits'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_no_memory_requests_usage_limit(*,
                                       host: str = None,
                                       api_key: str = None,
                                       username: str = None,
                                       password: str = None,
                                       **kwargs):
    """
    Check if the pod containers do not have a memory requests usage limit.

    Enforcing memory requests aids a fair balancing of resources across the
    cluster.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pods that do not have a memory requests
                 usage limits.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pods do not set memory requests usage limits.'
    msg_closed: str = 'Pods set memory requests usage limits.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for container in pod.spec.containers:
            limits = container.resources.requests
            (vulns if not limits or not limits.get('memory', None) else
             safes).append((f'{pod.metadata.self_link}',
                            'Must set memory requests usage limits'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_no_cpu_requests_usage_limit(*,
                                    host: str = None,
                                    api_key: str = None,
                                    username: str = None,
                                    password: str = None,
                                    **kwargs):
    """
    Check if the pod containers do not have CPU requests usage limits.

    Enforcing CPU requests aids a fair balancing of resources across the
    cluster.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pods that do not have CPU requests
                 usage limits.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pods do not set CPU requests usage limits.'
    msg_closed: str = 'Pods set CPU requests usage limits.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for container in pod.spec.containers:
            limits = container.resources.limits
            (vulns if not limits or not limits.get('cpu', None) else
             safes).append((f'{pod.metadata.self_link}',
                            'Must set CPU requests usage limits'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_add_cap_with_sys_admin(*,
                               host: str = None,
                               api_key: str = None,
                               username: str = None,
                               password: str = None,
                               **kwargs):
    """
    Check if there are pod containers with ``SYS_ADMIN`` in ADD capabilities.

    Capabilities permit certain named root actions without giving full root
    access. They are a more fine-grained permissions model, and all
    capabilities should be dropped from a pod, with only those required added
    back.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pods containers that have
                 ``SYS_ADMIN`` in ADD capabilities.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod containers have SYS_ADMIN in ADD capabilities.'
    msg_closed: str = \
        'Pod containers do not have SYS_ADMIN in ADD capabilities.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for container in pod.spec.containers:
            context = container.security_context
            if context and context.capabilities:
                (vulns if 'SYS_ADMIN' in context.capabilities.add else
                 safes).append((pod.metadata.self_link,
                                'SYS_ADMIN it’s equivalent to root'))
    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_containers_that_can_write_root_file_system(*,
                                                   host: str = None,
                                                   api_key: str = None,
                                                   username: str = None,
                                                   password: str = None):
    """
    Check if there are pod containers that can write to the root file system.

    An immutable root filesystem can prevent malicious binaries being added to
    PATH and increase attack cost.

    An immutable root filesystem prevents applications from writing to their
    local disk. This is desirable in the event of an intrusion as the attacker
    will not be able to tamper with the filesystem or write foreign executables
    to disk.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod containers that can write to the root
                 file system.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod containers can write to the root file system.'
    msg_closed: str = 'Pod containers can not write to the root file system.'

    attribute = {'read_only_root_filesystem': lambda x: x is False}
    safes = []

    vulns, safes = _check_security_context_attribute(
        host=host,
        api_key=api_key,
        username=username,
        password=password,
        attribute_check=attribute)

    message = 'must set read_only_root_filesystem to true'
    vulns = map(lambda x: (x, message), vulns)
    safes = map(lambda x: (x, message), safes)

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_pod_containers_that_run_as_root_user(*,
                                             host: str = None,
                                             api_key: str = None,
                                             username: str = None,
                                             password: str = None):
    """
    Check if there are pod containers that run as root user.

    Force the running image to run as a non-root user to ensure least
    privilege.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod containers that run as root user.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod containers run as root user.'
    msg_closed: str = 'Pod containers run as non root user.'

    attribute = {'run_as_non_root': lambda x: x is False}
    safes = []

    vulns, safes = _check_security_context_attribute(
        host=host,
        api_key=api_key,
        username=username,
        password=password,
        attribute_check=attribute)

    message = 'must set run_as_non_root to true'
    vulns = map(lambda x: (x, message), vulns)
    safes = map(lambda x: (x, message), safes)

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_pod_containers_that_allow_privilege_escalation(*,
                                                       host: str = None,
                                                       api_key: str = None,
                                                       username: str = None,
                                                       password: str = None):
    """
    Check if there are pod containers that allow privilege escalation.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are pod containers that allow privilege
                 escalation.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod containers allow privilege escalation.'
    msg_closed: str = 'Pod containers do not allow privilege escaltion.'

    attribute = {'allow_privilege_escalation': lambda x: x is True}
    safes = []

    vulns, safes = _check_security_context_attribute(
        host=host,
        api_key=api_key,
        username=username,
        password=password,
        attribute_check=attribute)

    message = 'must set allow_privilege_escalation to false'
    vulns = map(lambda x: (x, message), vulns)
    safes = map(lambda x: (x, message), safes)

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_volumes_mounted_in_docker_socket_path(*,
                                              host: str = None,
                                              api_key: str = None,
                                              username: str = None,
                                              password: str = None,
                                              **kwargs):
    """
    Check if there are containers with volumes mounted in docker socket path.

    Mounting the docker.socket leaks information about other containers and can
    allow container breakout.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are containers with volumes mounted in docker
                 socket path.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = \
        'Pod containers have volumes mounted in docker socket path.'
    msg_closed: str = \
        'Pod containers do not have volumes mounted in docker socket path.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        for index, volume in enumerate(pod.spec.volumes or []):
            (vulns if '/var/run/docker.sock' in volume.host_path.path else
             safes).append((f'{pod.metadata.self_link} spec.volumes[{index}]',
                            'Do not mount volumes in the docker socket path'))
    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)


@api(risk=LOW, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def has_containers_with_host_ipc_enabled(*,
                                         host: str = None,
                                         api_key: str = None,
                                         username: str = None,
                                         password: str = None,
                                         **kwargs):
    """
    Check if there are containers that have HostIPC enable.

    Sharing the host's IPC namespace allows container processes to communicate
    with processes on the host.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are containers that have HostIPC enabled.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Pod containers have hostIPC enable.'
    msg_closed: str = 'Pod containers do not have hostIPC enabled.'
    vulns, safes = [], []

    api_instance = _get_api_instance('CoreV1Api', host, api_key, username,
                                     password, **kwargs)
    pods = run_function(api_instance, 'list_pod_for_all_namespaces').items
    for pod in filter(lambda x: x.metadata.namespace != 'kube-system', pods):
        (vulns if pod.spec.host_ipc else
         safes).append((pod.metadata.self_link, 'must set host_ipc to false'))

    return _get_result_as_tuple(
        host=host,
        objects='Pods',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
