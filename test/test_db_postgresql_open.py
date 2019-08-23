# -*- coding: utf-8 -*-

"""Test module for fluidasserts.db.postgresql."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import postgresql


# Constants

DBNAME: str = 'dbname'
USER: str = 'user'
PASSWORD: str = 'password'
PORT = 5432


#
# Tests
#

@pytest.mark.parametrize('get_mock_ip', ['postgresql_weak'], indirect=True)
def test_have_access_open(get_mock_ip):
    """Test postgresql.have_access."""
    assert postgresql.have_access(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_open()
