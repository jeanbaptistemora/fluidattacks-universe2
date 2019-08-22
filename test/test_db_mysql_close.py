# -*- coding: utf-8 -*-

"""Test module for mysql_os."""

# standard imports
from __future__ import print_function

# 3rd party imports
import pytest

# local imports
from fluidasserts.db import mysql


# Constants

ADMIN_USER = 'root'
ADMIN_PASS = 'iethohnei2EeSh4P'
OS_PORT = 3306
NON_EXISTANT = '0.0.0.0'


#
# Close tests
#


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_have_access_close(get_mock_ip):
    """Check if there is access to MySQL server."""
    assert not mysql.have_access(NON_EXISTANT, ADMIN_USER, ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_test_db_present_close(get_mock_ip):
    """Check if MySQL 'test' DB is present."""
    # assert not mysql_db.test_db_exists(get_mock_ip, ADMIN_USER, ADMIN_PASS)
    assert not mysql.test_db_exists(NON_EXISTANT, ADMIN_USER, ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_local_infile_close(get_mock_ip):
    """Check if MySQL 'local_infile' is on."""
    # assert not mysql_db.local_infile_enabled(get_mock_ip, ADMIN_USER,
    #                                         ADMIN_PASS)
    assert not mysql.local_infile_enabled(NON_EXISTANT, ADMIN_USER,
                                          ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_symlinks_enabled_close(get_mock_ip):
    """Check if MySQL symlinks are enabled."""
    # assert not mysql_db.symlinks_enabled(get_mock_ip, ADMIN_USER,
    #                                         ADMIN_PASS)
    assert not mysql.symlinks_enabled(NON_EXISTANT, ADMIN_USER,
                                      ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_memcached_enabled_close(get_mock_ip):
    """Check if MySQL memcached is enabled."""
    assert not mysql.memcached_enabled(get_mock_ip, ADMIN_USER,
                                       ADMIN_PASS)
    assert not mysql.memcached_enabled(NON_EXISTANT, ADMIN_USER,
                                       ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_secure_file_close(get_mock_ip):
    """Check if MySQL secure_file_priv is enabled."""
    # assert not mysql_db.secure_file_priv_disabled(get_mock_ip, ADMIN_USER,
    #                                      ADMIN_PASS)
    assert not mysql.secure_file_priv_disabled(NON_EXISTANT, ADMIN_USER,
                                               ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_strict_all_tables_close(get_mock_ip):
    """Check if STRICT_ALL_TABLES are enabled."""
    # assert not mysql_db.strict_all_tables_disabled(get_mock_ip, ADMIN_USER,
    #                                      ADMIN_PASS)
    assert not mysql.strict_all_tables_disabled(NON_EXISTANT, ADMIN_USER,
                                                ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_log_error_close(get_mock_ip):
    """Check if MySQL log_error is enabled."""
    assert not mysql.log_error_disabled(NON_EXISTANT, ADMIN_USER,
                                        ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_logs_on_systemfs_close(get_mock_ip):
    """Check if MySQL logs on system filesystems are enabled."""
    # assert not mysql_db.logs_on_system_fs(get_mock_ip, ADMIN_USER,
    #                                      ADMIN_PASS)
    assert not mysql.logs_on_system_fs(NON_EXISTANT, ADMIN_USER,
                                       ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_logs_verbosity_close(get_mock_ip):
    """Check if MySQL logs have low verbosity."""
    # assert not mysql_db.logs_verbosity_low(get_mock_ip, ADMIN_USER,
    #                                      ADMIN_PASS)
    assert not mysql.logs_verbosity_low(NON_EXISTANT, ADMIN_USER,
                                        ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_auto_creates_users_close(get_mock_ip):
    """Check if MySQL auto creates users."""
    assert not mysql.auto_creates_users(get_mock_ip, ADMIN_USER,
                                        ADMIN_PASS)
    assert not mysql.auto_creates_users(NON_EXISTANT, ADMIN_USER,
                                        ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_users_without_pass_close(get_mock_ip):
    """Check if MySQL users have passwords."""
    assert not mysql.has_users_without_password(get_mock_ip, ADMIN_USER,
                                                ADMIN_PASS)
    assert not mysql.has_users_without_password(NON_EXISTANT, ADMIN_USER,
                                                ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_password_expiration_close(get_mock_ip):
    """Check if MySQL password expiration is safe."""
    assert not mysql.password_expiration_unsafe(NON_EXISTANT, ADMIN_USER,
                                                ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_password_equals_to_user_close(get_mock_ip):
    """Check if MySQL users have password equal to the username."""
    assert not mysql.password_equals_to_user(get_mock_ip, ADMIN_USER,
                                             ADMIN_PASS)
    assert not mysql.password_equals_to_user(NON_EXISTANT, ADMIN_USER,
                                             ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_wildcard_hosts_close(get_mock_ip):
    """Check if MySQL users have wildcard hosts."""
    assert not mysql.users_have_wildcard_host(NON_EXISTANT, ADMIN_USER,
                                              ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_uses_ssl_close(get_mock_ip):
    """Check if MySQL uses SSL."""
    # assert not mysql_db.uses_ssl(get_mock_ip, ADMIN_USER, ADMIN_PASS)
    assert not mysql.not_use_ssl(NON_EXISTANT, ADMIN_USER, ADMIN_PASS)


@pytest.mark.parametrize('get_mock_ip', ['mysql_db_hard'], indirect=True)
def test_ssl_forced_close(get_mock_ip):
    """Check if MySQL users forced to use SSL."""
    # assert not mysql_db.ssl_unforced(get_mock_ip, ADMIN_USER, ADMIN_PASS)
    assert not mysql.ssl_unforced(NON_EXISTANT, ADMIN_USER, ADMIN_PASS)
