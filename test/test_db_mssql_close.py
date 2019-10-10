# -*- coding: utf-8 -*-
"""Test module for fluidasserts.db.mssql."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import mssql

# Constants

DBNAME: str = 'test_db'
ADMIN_USER = 'SA'
ADMIN_PASSWORD = 'fluidasserts123.'
USER: str = 'test_user'
PASSWORD: str = 'Fluid1234.'
WRONG_PASSWORD = 'Fluid1234'
PORT = 1433

#
# Tests
#


@pytest.mark.parametrize('get_mock_ip', ['mssql_hard'], indirect=True)
def test_have_access_closed(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(DBNAME, USER, WRONG_PASSWORD, get_mock_ip,
                             PORT).is_closed()


@pytest.mark.parametrize('get_mock_ip', ['mssql_hard'], indirect=True)
def test_has_text_closed(get_mock_ip):
    """Test mssql.has_text."""
    assert mssql.has_text(DBNAME, ADMIN_USER, ADMIN_PASSWORD, get_mock_ip,
                             PORT, 'select * from users', 'fluidasserts123.').is_closed()


#
# UNKNOWN
#


@pytest.mark.parametrize('get_mock_ip', ['mssql_hard'], indirect=True)
def test_have_access_unknown(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(DBNAME, ADMIN_USER, ADMIN_PASSWORD, '0.0.0.0',
                             PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['mssql_hard'], indirect=True)
def test_has_text_unknown(get_mock_ip):
    """Test mssql.has_text."""
    assert mssql.has_text(DBNAME, ADMIN_USER, ADMIN_PASSWORD, '0.0.0.0',
                             PORT, 'select * from users', 'fluidasserts123.').is_unknown()
