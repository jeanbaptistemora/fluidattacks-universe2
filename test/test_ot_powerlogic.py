# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.ot packages."""

# standard imports
# None

# 3rd party imports
# None

# local imports
from fluidasserts.ot import powerlogic

#
# Constants
#

MOCK_SERVICE = 'http://localhost:5000'
NONEXISTANT_SERVICE = 'http://10.10.10.10'

#
# Open tests
#


def test_default_creds_open():
    """Check if Powerlogic PM800 has default credentials."""
    url = MOCK_SERVICE + '/pm800_default_creds/fail'
    assert powerlogic.pm800_has_default_credentials(url)


#
# Closing tests
#


def test_default_creds_close():
    """Check if Powerlogic PM800 has default credentials."""
    url = MOCK_SERVICE + '/pm800_default_creds/ok'
    assert not powerlogic.pm800_has_default_credentials(url)


def test_default_creds_unknown():
    """Check if Powerlogic PM800 has default credentials."""
    url = NONEXISTANT_SERVICE + '/ok'
    assert not powerlogic.pm800_has_default_credentials(url)
