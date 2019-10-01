# -*- coding: utf-8 -*-
"""Test module for fluidasserts.db.mssql."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import mssql

# Constants

DBNAME: str = 'mssql'
ADMIN_USER = 'SA'
ADMIN_PASSWORD = 'fluidasserts123.'
USER: str = 'mssql'
PASSWORD: str = 'Fluid1234.'
PORT = 1433


#
# Tests
#


@pytest.mark.parametrize('get_mock_ip', ['mssql_weak'], indirect=True)
def test_have_access_open(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(DBNAME, USER, PASSWORD, get_mock_ip,
                             PORT).is_open()
