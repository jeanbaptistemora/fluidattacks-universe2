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


#
# Tests
#


@pytest.mark.parametrize('get_mock_ip', ['postgresql_weak'], indirect=True)
def test_have_access_open(get_mock_ip):
    """Test postgresql.have_access."""
    assert postgresql.have_access(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_open()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_weak'], indirect=True)
def test_does_not_support_ssl_open(get_mock_ip):
    """Test postgresql.does_not_support_ssl."""
    assert postgresql.does_not_support_ssl(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_open()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_weak'], indirect=True)
def test_has_not_logging_enabled_open(get_mock_ip):
    """Test postgresql.has_not_logging_enabled."""
    assert postgresql.has_not_logging_enabled(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_open()
