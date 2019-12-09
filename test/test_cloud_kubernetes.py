# -*- coding: utf-8 -*-
"""Test module for fluidasserts.cloud.kubernetes."""
# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.kubernetes import deployments, pods

KUBERNETES_API_SERVER = os.environ['KUBERNETES_API_SERVER']
KUBERNETES_API_TOKEN = os.environ['KUBERNETES_API_TOKEN']
BAD_KUBERNETES_API_SERVER = 'https://1.2.3.4:16443'
BAD_KUBERNETES_API_TOKEN = 'some-value'


#
# Open tests
#


def test_runs_one_replica_per_deployment_open():
    """Search deployments runing only one replica."""
    assert deployments.runs_one_replica_per_deployment(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


def test_privileged_containers_open():
    """Search privileged containers."""
    assert pods.privileged_containers(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


#
# Closing tests
#


def test_undefined_pod_security_policies_closed():
    """Check pod security policies are undefined."""
    assert pods.undefined_pod_security_policies(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN).is_closed()
    assert pods.undefined_pod_security_policies(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_TOKEN).is_unknown()
