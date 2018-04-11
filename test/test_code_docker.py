# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.code.docker."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.code import docker
import fluidasserts.utils.decorators

# Constants
fluidasserts.utils.decorators.UNITTEST = True
CODE_DIR = 'test/static/code/docker/'
SECURE_CODE = CODE_DIR + 'Dockerfile.close'
INSECURE_CODE = CODE_DIR + 'Dockerfile.open'


#
# Open tests
#


def test_not_pinned_open():
    """Search for pinned dockerfile."""
    assert docker.not_pinned(INSECURE_CODE)

#
# Closing tests
#


def test_not_pinned_close():
    """Search for pinned dockerfile."""
    assert not docker.not_pinned(SECURE_CODE)
