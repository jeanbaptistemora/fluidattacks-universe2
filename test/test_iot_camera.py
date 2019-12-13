# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.iot packages."""

# standard imports
import os
import contextlib

# 3rd party imports
import pytest
pytestmark = pytest.mark.iot

# local imports
from fluidasserts.iot import camera

#
# Constants
#

WEAK_CAMERA: str = 'http://localhost:9001'
HARD_CAMERA: str = 'http://localhost:9002'


@contextlib.contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ['HTTP_PROXY'] = '127.0.0.1:8080'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:8080'
    try:
        yield
    finally:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)

#
# Open tests
#


def test_axis_rce_open():
    """Check if Axis Camera is vulnerable to RCE."""
    assert camera.axis_has_rce(WEAK_CAMERA)

#
# Closing tests
#


def test_axis_rce_close():
    """Check if Axis Camera is vulnerable to RCE."""
    assert not camera.axis_has_rce(HARD_CAMERA)

    with no_connection():
        assert not camera.axis_has_rce(HARD_CAMERA)
