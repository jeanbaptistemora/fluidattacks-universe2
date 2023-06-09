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
WRONG_PASSWORD = "Fluid1234"
PORT = 1433
BAD_HOST = "0.0.0.1"

#
# Tests
#


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_have_access_closed(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(
        USER, WRONG_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_text_closed(get_mock_ip):
    """Test mssql.has_text."""
    assert mssql.has_text(
        DBNAME,
        ADMIN_USER,
        ADMIN_PASSWORD,
        get_mock_ip,
        PORT,
        "select * from users",
        "fluidasserts123.",
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_login_password_expiration_disabled_closed(get_mock_ip):
    """Test mssql.has_login_password_expiration_disabled."""
    assert mssql.has_login_password_expiration_disabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_enabled_ad_hoc_queries_closed(get_mock_ip):
    """Test mssql.has_enabled_ad_hoc_queries."""
    assert mssql.has_enabled_ad_hoc_queries(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_alter_any_database_closed(get_mock_ip):
    """Test mssql.can_alter_any_database."""
    assert mssql.can_alter_any_database(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_password_policy_check_disabled_closed(get_mock_ip):
    """Test mssql.has_password_policy_check_disabled."""
    assert mssql.has_password_policy_check_disabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_xps_option_enabled_closed(get_mock_ip):
    """Test mssql.has_xps_option_enabled."""
    assert mssql.has_xps_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_asymmetric_keys_with_unencrypted_private_keys_closed(get_mock_ip):
    """Test mssql.has_asymmetric_keys_with_unencrypted_private_keys."""
    assert mssql.has_asymmetric_keys_with_unencrypted_private_keys(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_smo_and_dmo_xps_option_enabled_closed(get_mock_ip):
    """Test mssql.has_smo_and_dmo_xps_option_enabled."""
    assert mssql.has_smo_and_dmo_xps_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_contained_dbs_with_auto_close_enabled_closed(get_mock_ip):
    """Test mssql.has_contained_dbs_with_auto_close_enabled."""
    assert mssql.has_contained_dbs_with_auto_close_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_alter_any_login_closed(get_mock_ip):
    """Test mssql.can_alter_any_login."""
    assert mssql.can_alter_any_login(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_control_server_closed(get_mock_ip):
    """Test mssql.can_control_server."""
    assert mssql.can_control_server(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_alter_any_credential_closed(get_mock_ip):
    """Test mssql.can_alter_any_credential."""
    assert mssql.can_alter_any_credential(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_unencrypted_storage_procedures_closed(get_mock_ip):
    """Test mssql.has_unencrypted_storage_procedures."""
    assert mssql.has_unencrypted_storage_procedures(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_shutdown_server_closed(get_mock_ip):
    """Test mssql.can_shutdown_server."""
    assert mssql.can_shutdown_server(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_clr_option_enabled_closed(get_mock_ip):
    """Test mssql.has_clr_option_enabled."""
    assert mssql.has_clr_option_enabled(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_trustworthy_status_on_closed(get_mock_ip):
    """Test mssql.has_trustworthy_status_on."""
    assert mssql.has_trustworthy_status_on(
        ADMIN_USER, ADMIN_PASSWORD, get_mock_ip, PORT
    ).is_closed()


#
# UNKNOWN
#


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_have_access_unknown(get_mock_ip):
    """Test mssql.have_access."""
    assert mssql.have_access(
        ADMIN_USER, ADMIN_PASSWORD, "0.0.0.0", PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_text_unknown(get_mock_ip):
    """Test mssql.has_text."""
    assert mssql.has_text(
        DBNAME,
        ADMIN_USER,
        ADMIN_PASSWORD,
        BAD_HOST,
        PORT,
        "select * from users",
        "fluidasserts123.",
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_login_password_expiration_disabled_unknown(get_mock_ip):
    """Test mssql.has_login_password_expiration_disabled."""
    assert mssql.has_login_password_expiration_disabled(
        ADMIN_USER, WRONG_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_enabled_ad_hoc_queries_unknown(get_mock_ip):
    """Test mssql.has_enabled_ad_hoc_queries."""
    assert mssql.has_enabled_ad_hoc_queries(
        ADMIN_USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_alter_any_database_unknown(get_mock_ip):
    """Test mssql.can_alter_any_database."""
    assert mssql.can_alter_any_database(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_password_policy_check_disabled_unknown(get_mock_ip):
    """Test mssql.has_password_policy_check_disabled."""
    assert mssql.has_password_policy_check_disabled(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_xps_option_enabled_unknown(get_mock_ip):
    """Test mssql.has_xps_option_enabled."""
    assert mssql.has_xps_option_enabled(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_asymmetric_keys_with_unencrypted_private_keys_unknown(
    get_mock_ip,
):
    """Test mssql.has_asymmetric_keys_with_unencrypted_private_keys."""
    assert mssql.has_asymmetric_keys_with_unencrypted_private_keys(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_smo_and_dmo_xps_option_enabled_unknown(get_mock_ip):
    """Test mssql.has_smo_and_dmo_xps_option_enabled."""
    assert mssql.has_smo_and_dmo_xps_option_enabled(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_contained_dbs_with_auto_close_enabled_unknown(get_mock_ip):
    """Test mssql.has_contained_dbs_with_auto_close_enabled."""
    assert mssql.has_contained_dbs_with_auto_close_enabled(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_alter_any_login_unknown(get_mock_ip):
    """Test mssql.can_alter_any_login."""
    assert mssql.can_alter_any_login(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_control_server_unknown(get_mock_ip):
    """Test mssql.can_control_server."""
    assert mssql.can_control_server(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_alter_any_credential_unknown(get_mock_ip):
    """Test mssql.can_alter_any_credential."""
    assert mssql.can_alter_any_credential(
        USER, ADMIN_PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_sa_account_login_enabled_unknown(get_mock_ip):
    """Test mssql.has_sa_account_login_enabled."""
    assert mssql.has_sa_account_login_enabled(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_remote_access_option_enabled_unknown(get_mock_ip):
    """Test mssql.has_remote_access_option_enabled."""
    assert mssql.has_remote_access_option_enabled(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_unencrypted_storage_procedures_unknown(get_mock_ip):
    """Test mssql.has_unencrypted_storage_procedures."""
    assert mssql.has_unencrypted_storage_procedures(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_can_shutdown_server_unknown(get_mock_ip):
    """Test mssql.can_shutdown_server."""
    assert mssql.can_shutdown_server(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_sa_account_has_not_been_renamed_unknown(get_mock_ip):
    """Test mssql.sa_account_has_not_been_renamed."""
    assert mssql.sa_account_has_not_been_renamed(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_clr_option_enabled_unknown(get_mock_ip):
    """Test mssql.has_clr_option_enabled."""
    assert mssql.has_clr_option_enabled(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()


@pytest.mark.parametrize("get_mock_ip", ["mssql_hard"], indirect=True)
def test_has_trustworthy_status_on_unknown(get_mock_ip):
    """Test mssql.has_trustworthy_status_on."""
    assert mssql.has_trustworthy_status_on(
        USER, PASSWORD, BAD_HOST, PORT
    ).is_unknown()
