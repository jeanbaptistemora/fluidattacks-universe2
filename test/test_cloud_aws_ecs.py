# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('cloud')

# local imports
from fluidasserts.cloud.aws import ecs


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#

def test_has_not_resources_usage_limits_open():
    """Search tasks with unlimited containers usage resources."""
    assert ecs.has_not_resources_usage_limits(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY).is_open()


def test_write_root_file_system_open():
    """Search tasks that allow write in the root file system."""
    assert ecs.write_root_file_system(AWS_ACCESS_KEY_ID,
                                      AWS_SECRET_ACCESS_KEY).is_open()


def test_no_iam_role_for_tasks_open():
    """Search for tasks that do not use IAM roles."""
    assert ecs.no_iam_role_for_tasks(AWS_ACCESS_KEY_ID,
                                     AWS_SECRET_ACCESS_KEY).is_open()


def test_run_containers_as_root_user_open():
    """Search for tasks that execute the container as root user."""
    assert ecs.run_containers_as_root_user(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY).is_open()


def test_write_volumes_open():
    """Search for tasks that that allow write in volumes."""
    assert ecs.write_volumes(AWS_ACCESS_KEY_ID,
                             AWS_SECRET_ACCESS_KEY).is_open()
