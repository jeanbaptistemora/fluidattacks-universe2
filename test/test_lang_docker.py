# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.docker."""

# standard imports
# None

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('lang')

# local imports
from fluidasserts.lang import docker


# Constants

CODE_DIR = 'test/static/lang/docker/'
SECURE_DIR = 'test/static/lang/docker/closed'
SECURE_CODE = [
    f'{SECURE_DIR}/1',
    f'{SECURE_DIR}/2',
    f'{SECURE_DIR}/3',
]
INSECURE_DIR = 'test/static/lang/docker/open'
INSECURE_CODE = [
    f'{INSECURE_DIR}/1',
    f'{INSECURE_DIR}/2',
    f'{INSECURE_DIR}/3',
    f'{INSECURE_DIR}/4',
]
NOT_EXISTANT_DIR = 'test/static/lang/docker/unknown'
NOT_EXISTANT_CODE = 'test/static/lang/docker/unknown/1'


#
# Open tests
#


def test_open_not_pinned():
    """Search for pinned dockerfile."""
    assert docker.not_pinned(INSECURE_DIR).is_open()
    for test in INSECURE_CODE:
        assert docker.not_pinned(test).is_open()


#
# Closing tests
#


def test_close_not_pinned():
    """Search for pinned dockerfile."""
    assert docker.not_pinned(SECURE_DIR).is_closed()
    for test in SECURE_CODE:
        assert docker.not_pinned(test).is_closed()
    assert docker.not_pinned(CODE_DIR, exclude=['test']).is_closed()

#
# Unknown tests
#

def test_unknown_not_pinned():
    """Search for pinned dockerfile."""
    assert docker.not_pinned(NOT_EXISTANT_DIR).is_unknown()
    assert docker.not_pinned(NOT_EXISTANT_CODE).is_unknown()
