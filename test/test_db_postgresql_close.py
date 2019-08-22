# -*- coding: utf-8 -*-

"""Test module for mysql_os."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import postgresql


# Constants

DBNAME: str = 'dbname'
USER: str = 'user'
PASSWORD: str = 'wrong password'
BAD_HOST: str = '0.0.0.0'
PORT = 5432


#
# Tests
#

@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_have_access_closed(get_mock_ip):
    """Test postgresql.have_access."""
    assert postgresql.have_access(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.have_access(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()
