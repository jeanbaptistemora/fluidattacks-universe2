# -*- coding: utf-8 -*-
"""Test module for fluidasserts.db.mssql."""


from fluidasserts.db import (
    mssql,
)
import pytest

pytestmark = pytest.mark.asserts_module("db_mssql")

# Constants

DBNAME: str = "test_db"
ADMIN_USER = "SA"
ADMIN_PASSWORD = "fluidasserts123."
USER: str = "test_user"
PASSWORD: str = "Fluid1234."
PORT = 1432


#
# Tests
#


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_have_access_open(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(USER, PASSWORD, get_mock_ip, PORT).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_text_open(get_mock_ip):
    """Test mssql.has_text."""
    assert mssql.has_text(
        DBNAME,
        ADMIN_USER,
        ADMIN_PASSWORD,
        get_mock_ip,
        PORT,
        "select * from users",
        "fluidasserts123.",
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_login_password_expiration_disabled_open(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.has_login_password_expiration_disabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_enabled_ad_hoc_queries_open(get_mock_ip):
    """Test mssql.has_enabled_ad_hoc_queries."""
    assert mssql.has_enabled_ad_hoc_queries(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_can_alter_any_database_open(get_mock_ip):
    """Test mssql.can_alter_any_database."""
    assert mssql.can_alter_any_database(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_password_policy_check_disabled_open(get_mock_ip):
    """Test mssql.has_password_policy_check_disabled."""
    assert mssql.has_password_policy_check_disabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_xps_option_enabled_open(get_mock_ip):
    """Test mssql.has_xps_option_enabled."""
    assert mssql.has_xps_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_asymmetric_keys_with_unencrypted_private_keys_open(get_mock_ip):
    """Test mssql.has_asymmetric_keys_with_unencrypted_private_keys."""
    assert mssql.has_asymmetric_keys_with_unencrypted_private_keys(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_smo_and_dmo_xps_option_enabled_open(get_mock_ip):
    """Test mssql.has_smo_and_dmo_xps_option_enabled."""
    assert mssql.has_smo_and_dmo_xps_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_contained_dbs_with_auto_close_enabled_open(get_mock_ip):
    """Test mssql.has_contained_dbs_with_auto_close_enabled."""
    assert mssql.has_contained_dbs_with_auto_close_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_can_alter_any_login_open(get_mock_ip):
    """Test mssql.can_alter_any_login."""
    assert mssql.can_alter_any_login(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_can_control_server_open(get_mock_ip):
    """Test mssql.can_control_server."""
    assert mssql.can_control_server(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_can_alter_any_credential_open(get_mock_ip):
    """Test mssql.can_alter_any_credential."""
    assert mssql.can_alter_any_credential(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_sa_account_login_enabled_open(get_mock_ip):
    """Test mssql.has_sa_account_login_enabled."""
    assert mssql.has_sa_account_login_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_remote_access_option_enabled_open(get_mock_ip):
    """Test mssql.has_remote_access_option_enabled."""
    assert mssql.has_remote_access_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_unencrypted_storage_procedures_open(get_mock_ip):
    """Test mssql.has_unencrypted_storage_procedures."""
    assert mssql.has_unencrypted_storage_procedures(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_can_shutdown_server_open(get_mock_ip):
    """Test mssql.can_shutdown_server."""
    assert mssql.can_shutdown_server(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_sa_account_has_not_been_renamed_open(get_mock_ip):
    """Test mssql.sa_account_has_not_been_renamed."""
    assert mssql.sa_account_has_not_been_renamed(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()


@pytest.mark.parametrize("get_mock_ip", ["mssql_weak"], indirect=True)
def test_has_clr_option_enabled_open(get_mock_ip):
    """Test mssql.has_clr_option_enabled."""
    assert mssql.has_clr_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_open()
