# -*- coding: utf-8 -*-
"""Test module for fluidasserts.db.mssql."""

# standard imports

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import mssql

# Constants

DBNAME: str = 'mssql'
USER: str = 'mssql'
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
