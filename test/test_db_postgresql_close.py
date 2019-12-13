# -*- coding: utf-8 -*-

"""Test module for fluidasserts.db.postgresql."""

# standard imports

# 3rd party imports
import pytest
pytestmark = pytest.mark.db

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
def test_others_closed(get_mock_ip):
    """Test others postgresql functions and things."""
    var_does_not_exist: str = 'var_does_not_exist'
    connection_string: str = postgresql.ConnectionString(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT, 'prefer')
    assert not postgresql._get_var(connection_string, var_does_not_exist)


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


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_has_not_logging_enabled_closed(get_mock_ip):
    """Test postgresql.has_not_logging_enabled."""
    assert postgresql.has_not_logging_enabled(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.has_not_logging_enabled(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_has_not_data_checksums_enabled_closed(get_mock_ip):
    """Test postgresql.has_not_data_checksums_enabled."""
    assert postgresql.has_not_data_checksums_enabled(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.has_not_data_checksums_enabled(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_has_insecure_password_encryption_closed(get_mock_ip):
    """Test postgresql.has_insecure_password_encryption."""
    assert postgresql.has_insecure_password_encryption(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.has_insecure_password_encryption(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_has_insecurely_stored_passwords_closed(get_mock_ip):
    """Test postgresql.has_insecurely_stored_passwords."""
    assert postgresql.has_insecurely_stored_passwords(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.has_insecurely_stored_passwords(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_has_insecure_file_permissions_closed(get_mock_ip):
    """Test postgresql.has_insecure_file_permissions."""
    assert postgresql.has_insecure_file_permissions(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.has_insecure_file_permissions(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_allows_too_many_concurrent_connections_closed(get_mock_ip):
    """Test postgresql.allows_too_many_concurrent_connections."""
    assert postgresql.allows_too_many_concurrent_connections(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.allows_too_many_concurrent_connections(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()


@pytest.mark.parametrize('get_mock_ip', ['postgresql_hard'], indirect=True)
def test_does_not_invalidate_session_ids_closed(get_mock_ip):
    """Test postgresql.does_not_invalidate_session_ids."""
    assert postgresql.does_not_invalidate_session_ids(
        DBNAME, USER, PASSWORD, get_mock_ip, PORT).is_closed()
    assert postgresql.does_not_invalidate_session_ids(
        DBNAME, USER, PASSWORD, BAD_HOST, PORT).is_unknown()
