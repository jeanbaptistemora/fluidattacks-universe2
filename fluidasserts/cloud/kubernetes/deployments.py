# -*- coding: utf-8 -*-
"""Kubernetes cloud checks deployments."""

# standard imports
from urllib3.exceptions import MaxRetryError

# local imports
from fluidasserts import DAST, MEDIUM
from fluidasserts.utils.decorators import api, unknown_if
from fluidasserts.cloud.kubernetes import _get_result_as_tuple, \
    _get_api_instance, run_function

# 3rd party imports
from kubernetes.client.rest import ApiException  # noqa


@api(risk=MEDIUM, kind=DAST)
@unknown_if(ApiException, MaxRetryError)
def runs_one_replica_per_deployment(*,
                                    host: str = None,
                                    api_key: str = None,
                                    username: str = None,
                                    password: str = None,
                                    **kwargs):
    """
    Check if run one replica for Deployment.

    Never run a single Pod individually.

    :param host: URL of the API server.
    :param api_key: API Key to make requests.
    :param username: Username of account.
    :param password: Password of account.

    :returns: - ``OPEN`` if there are deployments running only one replica.
              - ``UNKNOWN`` on errors.
              - ``CLOSED`` otherwise.

    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'Deployments are running only one replica.'
    msg_closed: str = 'Deployments run more than one replica.'
    vulns, safes = [], []

    api_instance = _get_api_instance('AppsV1Api',
                                     host, api_key,
                                     username,
                                     password,
                                     **kwargs)
    api_response = run_function(
        api_instance, 'list_deployment_for_all_namespaces')
    for deployment in api_response.items:
        (safes if deployment.status.replicas > 1 else vulns).append(
            (deployment.metadata.self_link,
             'Must run more than one replica per deployment.'))

    return _get_result_as_tuple(
        host=host,
        objects='Deployments',
        msg_open=msg_open,
        msg_closed=msg_closed,
        vulns=vulns,
        safes=safes)
