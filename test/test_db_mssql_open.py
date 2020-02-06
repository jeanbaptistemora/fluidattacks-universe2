# -*- coding: utf-8 -*-
"""Test module for fluidasserts.db.mssql."""

# standard imports

# 3rd party imports
import pytest
pytestmark = pytest.mark.asserts_module('db_mssql')


# local imports
from fluidasserts.db import mssql

# Constants

DBNAME: str = 'test_db'
ADMIN_USER = 'SA'
ADMIN_PASSWORD = 'fluidasserts123.'
USER: str = 'test_user'
PASSWORD: str = 'Fluid1234.'
PORT = 1432


#
# Tests
#


@pytest.mark.parametrize('get_mock_ip', ['mssql_weak'], indirect=True)
def test_have_access_open(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(DBNAME, USER, PASSWORD, get_mock_ip,
                             PORT).is_open()


@pytest.mark.parametrize('get_mock_ip', ['mssql_weak'], indirect=True)
def test_has_text_open(get_mock_ip):
    """Test mssql.has_text."""
    assert mssql.has_text(DBNAME, ADMIN_USER, ADMIN_PASSWORD, get_mock_ip,
                          PORT, 'select * from users',
                          'fluidasserts123.').is_open()


@pytest.mark.parametrize('get_mock_ip', ['mssql_weak'], indirect=True)
def test_has_login_password_expiration_disabled_open(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.has_login_password_expiration_disabled(
        DBNAME, ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT).is_open()
