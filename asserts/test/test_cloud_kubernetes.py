# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-
"""Test module for fluidasserts.cloud.kubernetes."""

import boto3
from fluidasserts.cloud.kubernetes import (
    deployments,
    pods,
)
import jmespath
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_kubernetes")


AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
BAD_KUBERNETES_API_SERVER = "https://1.2.3.4:16443"
BAD_KUBERNETES_API_TOKEN = "some-value"
AWS_EC2_INSTANCE = os.environ["AWS_EC2_INSTANCE"]
client = boto3.client(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)
try:
    HOST = jmespath.search(
        (
            f"Reservations[].Instances[?InstanceId=='{AWS_EC2_INSTANCE}']"
            ".NetworkInterfaces[][].Association.PublicIp"
        ),
        client.describe_instances(),
    )[0]
except IndexError:
    raise Exception(
        f"The instance {AWS_EC2_INSTANCE} does not "
        "have associated public IP address"
    )

KUBERNETES_API_SERVER = f"https://{HOST}:16443"
KUBERNETES_API_TOKEN = os.environ["KUBERNETES_API_TOKEN"]


#
# Open tests
#


def test_runs_one_replica_per_deployment_open():
    """Search deployments runing only one replica."""
    assert deployments.runs_one_replica_per_deployment(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_privileged_containers_open():
    """Search privileged containers."""
    assert pods.privileged_containers(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_write_root_file_system_open():
    """Search containers that write in root file system."""
    assert pods.write_root_file_system(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_privilege_escalation_open():
    """Search containers with privilege escalation."""
    assert pods.privilege_escalation(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_run_containers_as_root_user_open():
    """Search containers running as root user."""
    assert pods.run_containers_as_root_user(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_no_memory_usage_limits_open():
    """Search containers that do not have memory usage limits."""
    assert pods.has_no_memory_usage_limits(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_no_cpu_usage_limits_open():
    """Search containers that do not have CPU usage limits."""
    assert pods.has_no_cpu_usage_limits(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_no_memory_requests_usage_limit_open():
    """Search containers that do not have memory requests usage limits."""
    assert pods.has_no_memory_requests_usage_limit(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_no_cpu_requests_usage_limit_open():
    """Search containers that do not have CPU requests usage limits."""
    assert pods.has_no_cpu_requests_usage_limit(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_add_cap_with_sys_admin_open():
    """Search containers that have capabilities with sys_admin permissions."""
    assert pods.has_add_cap_with_sys_admin(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_containers_that_can_write_root_file_system_open():
    """Search containers that can writhe in the root file system."""
    assert pods.has_containers_that_can_write_root_file_system(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_pod_containers_that_run_as_root_user_open():
    """Search containers that run as root user."""
    assert pods.has_pod_containers_that_run_as_root_user(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_pod_containers_that_allow_privilege_escalation_open():
    """Search containers that allow privilege escalation."""
    assert pods.has_pod_containers_that_allow_privilege_escalation(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_volumes_mounted_in_docker_socket_path_open():
    """Search deployments that have volumes mounted in docker socket path."""
    assert pods.has_volumes_mounted_in_docker_socket_path(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


def test_has_containers_with_host_ipc_enabled_open():
    """Search containers that have IPC enabled."""
    assert pods.has_containers_with_host_ipc_enabled(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_open()


#
# Closing tests
#


def test_run_containers_as_root_user_closed():
    """Search containers running as root user."""
    assert pods.run_containers_as_root_user(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_privilege_escalation_closed():
    """Search containers with privilege escalation."""
    assert pods.privilege_escalation(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_write_root_file_system_closed():
    """Search containers that write in root file system."""
    assert pods.write_root_file_system(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_privileged_containers_close():
    """Search privileged containers."""
    assert pods.privileged_containers(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_undefined_pod_security_policies_closed():
    """Check pod security policies are undefined."""
    assert pods.undefined_pod_security_policies(
        host=KUBERNETES_API_SERVER, api_key=KUBERNETES_API_TOKEN
    ).is_closed()
    assert pods.undefined_pod_security_policies(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_TOKEN
    ).is_unknown()


def test_has_no_memory_usage_limits_close():
    """Search containers that do not have memory usage limits."""
    assert pods.has_no_memory_usage_limits(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_no_cpu_usage_limits_close():
    """Search containers that do not have CPU usage limits."""
    assert pods.has_no_cpu_usage_limits(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_no_memory_requests_usage_limit_close():
    """Search containers that do not have memory requests usage limits."""
    assert pods.has_no_memory_requests_usage_limit(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_no_cpu_requests_usage_limit_close():
    """Search containers that do not have CPU requests usage limits."""
    assert pods.has_no_cpu_requests_usage_limit(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_add_cap_with_sys_admin_close():
    """Search containers that have capabilities with sys_admin permissions."""
    assert pods.has_add_cap_with_sys_admin(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_containers_that_can_write_root_file_system_close():
    """Search containers that can writhe in the root file system."""
    assert pods.has_containers_that_can_write_root_file_system(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_pod_containers_that_run_as_root_user_close():
    """Search containers that run as root user."""
    assert pods.has_pod_containers_that_run_as_root_user(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_pod_containers_that_allow_privilege_escalation_close():
    """Search containers that allow privilege escalation."""
    assert pods.has_pod_containers_that_allow_privilege_escalation(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_volumes_mounted_in_docker_socket_path_close():
    """Search deployments that have volumes mounted in docker socket path."""
    assert pods.has_volumes_mounted_in_docker_socket_path(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()


def test_has_containers_with_host_ipc_enabled_close():
    """Search containers that have IPC enabled."""
    assert pods.has_containers_with_host_ipc_enabled(
        host=BAD_KUBERNETES_API_SERVER, api_key=BAD_KUBERNETES_API_SERVER
    ).is_unknown()
