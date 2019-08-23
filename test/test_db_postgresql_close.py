# -*- coding: utf-8 -*-

"""Test module for fluidasserts.db.postgresql."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import postgresql


# Constants

DBNAME: str = 'postgres'
USER: str = 'postgres'
PASSWORD: str = 'postgres'
PORT = 5432

BAD_HOST: str = '0.0.0.0'
BAD_PASSWORD: str = 'wrong password'


#
# Tests
#


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_have_access_closed(get_mock_ip):
    """Test postgresql.have_access."""
    assert postgresql.have_access(
        DBNAME, USER, BAD_PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.have_access(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_does_not_support_ssl_closed(get_mock_ip):
    """Test postgresql.does_not_support_ssl."""
    assert postgresql.does_not_support_ssl(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.does_not_support_ssl(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()
