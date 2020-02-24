# -*- coding: utf-8 -*-
"""Test module for fluidasserts.cloud.kubernetes."""
# standard imports
from fluidasserts.cloud.kubernetes import deployments, pods
import os

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud_kubernetes')

# local imports

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


def test_write_root_file_system_open():
    """Search containers that write in root file system."""
    assert pods.write_root_file_system(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


def test_privilege_escalation_open():
    """Search containers with privilege escalation."""
    assert pods.privilege_escalation(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


def test_run_containers_as_root_user_open():
    """Search containers running as root user."""
    assert pods.run_containers_as_root_user(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


def test_has_no_memory_usage_limits_open():
    """Search containers that do not have memory usage limits."""
    assert pods.has_no_memory_usage_limits(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


def test_has_no_cpu_usage_limits_open():
    """Search containers that do not have CPU usage limits."""
    assert pods.has_no_cpu_usage_limits(
        host=KUBERNETES_API_SERVER,
        api_key=KUBERNETES_API_TOKEN).is_open()


#
# Closing tests
#


def test_run_containers_as_root_user_closed():
    """Search containers running as root user."""
    assert pods.run_containers_as_root_user(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_SERVER).is_unknown()


def test_privilege_escalation_closed():
    """Search containers with privilege escalation."""
    assert pods.privilege_escalation(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_SERVER).is_unknown()


def test_write_root_file_system_closed():
    """Search containers that write in root file system."""
    assert pods.write_root_file_system(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_SERVER).is_unknown()


def test_privileged_containers_close():
    """Search privileged containers."""
    assert pods.privileged_containers(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_SERVER).is_unknown()


def test_undefined_pod_security_policies_closed():
    """Check pod security policies are undefined."""
    assert pods.undefined_pod_security_policies(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN).is_closed()
    assert pods.undefined_pod_security_policies(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_TOKEN).is_unknown()


def test_has_no_memory_usage_limits_close():
    """Search containers that do not have memory usage limits."""
    assert pods.has_no_memory_usage_limits(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_SERVER).is_unknown()


def test_has_no_cpu_usage_limits_close():
    """Search containers that do not have CPU usage limits."""
    assert pods.has_no_cpu_usage_limits(
        host=BAD_KUBERNETES_API_SERVER,
        api_key=BAD_KUBERNETES_API_SERVER).is_unknown()
