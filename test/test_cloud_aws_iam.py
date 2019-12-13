# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os
from contextlib import contextmanager

# 3rd party imports
import pytest
pytestmark = pytest.mark.cloud

# local imports
from fluidasserts.cloud.aws import iam


# Constants
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ['HTTP_PROXY'] = '127.0.0.1:8080'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:8080'
    try:
        yield
    finally:
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)


#
# Open tests
#


def test_pass_len_unsafe_open():
    """Search IAM policy: Password length requirement."""
    assert iam.min_password_len_unsafe(AWS_ACCESS_KEY_ID,
                                       AWS_SECRET_ACCESS_KEY)


def test_pass_reuse_unsafe_open():
    """Search IAM policy: Password reuse requirement."""
    assert iam.password_reuse_unsafe(AWS_ACCESS_KEY_ID,
                                     AWS_SECRET_ACCESS_KEY)


def test_pass_expiration_unsafe_open():
    """Search IAM policy: Password expiration requirement."""
    assert iam.password_expiration_unsafe(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)


def test_root_mfa_open():
    """Search IAM summary: MFA for root."""
    assert iam.root_without_mfa(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_not_support_role_open():
    """Search IAM policy: Support role."""
    assert iam.has_not_support_role(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_policies_attached_open():
    """Search IAM policies: Policies attached directly to users."""
    assert iam.policies_attached_to_users(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY).is_open()


def test_have_old_access_keys_open():
    """Search old access keys."""
    assert iam.have_old_access_keys(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY).is_open()


def test_has_root_active_signing_certificates_open():
    """Search root user with signing certificates activated."""
    assert iam.has_root_active_signing_certificates(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_users_with_password_and_access_keys_open():
    """Search users whit users with password and access keys activated."""
    assert iam.users_with_password_and_access_keys(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_group_with_inline_policies_open():
    """Search IAM groups with inline policies."""
    assert iam.group_with_inline_policies(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_mfa_disabled_for_users_with_console_password_open():
    """Search IAM users with with console password and MFA disabled."""
    assert iam.mfa_disabled_for_users_with_console_password(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_has_wildcard_resource_on_write_action_open():
    """Search iam policies with wildcard resources in write actions."""
    assert iam.has_wildcard_resource_on_write_action(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_has_privileges_over_iam_open():
    """Search iam policies with privileges over iam."""
    assert iam.has_privileges_over_iam(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


def test_users_with_multiple_access_keys_open():
    """Search users with multiples access keys."""
    assert iam.users_with_multiple_access_keys(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).is_open()


#
# Closing tests
#


def test_has_old_ssh_public_keys_close():
    """Search olds ssh public keys."""
    assert iam.has_old_ssh_public_keys(AWS_ACCESS_KEY_ID,
                                       AWS_SECRET_ACCESS_KEY).is_closed()
    assert iam.has_old_ssh_public_keys(AWS_ACCESS_KEY_ID,
                                       AWS_SECRET_ACCESS_KEY_BAD,
                                       retry=False).is_unknown()


def test_has_permissive_role_policies_closed():
    """Search roles with permissive policies."""
    assert iam.has_permissive_role_policies(AWS_ACCESS_KEY_ID,
                                            AWS_SECRET_ACCESS_KEY).is_closed()
    assert iam.has_permissive_role_policies(AWS_ACCESS_KEY_ID,
                                            AWS_SECRET_ACCESS_KEY_BAD,
                                            retry=False).is_unknown()


def test_has_mfa_disabled_close():
    """Search MFA on IAM users."""
    assert not iam.has_mfa_disabled(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY)
    assert not iam.has_mfa_disabled(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY_BAD,
                                    retry=False)
    with no_connection():
        assert not iam.has_mfa_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_have_old_creds_enabled_close():
    """Search old unused passwords."""
    assert not iam.have_old_creds_enabled(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    assert not iam.have_old_creds_enabled(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY_BAD,
                                          retry=False)
    with no_connection():
        assert not iam.have_old_creds_enabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_have_old_access_keys_close():
    """Search old access keys."""
    assert not iam.have_old_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)
    with no_connection():
        assert not iam.have_old_access_keys(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_root_has_access_keys_close():
    """Search root access keys."""
    assert not iam.root_has_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.root_has_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)
    with no_connection():
        assert not iam.root_has_access_keys(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_not_requires_uppercase_close():
    """Search IAM policy: Uppercase letter requirement."""
    assert not iam.not_requires_uppercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_uppercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY_BAD,
                                          retry=False)

    with no_connection():
        assert not iam.not_requires_uppercase(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_not_requires_lowercase_close():
    """Search IAM policy: Lowercase letter requirement."""
    assert not iam.not_requires_lowercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_lowercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY_BAD,
                                          retry=False)
    with no_connection():
        assert not iam.not_requires_lowercase(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_not_requires_symbols_close():
    """Search IAM policy: Symbols requirement."""
    assert not iam.not_requires_symbols(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_symbols(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)
    with no_connection():
        assert not iam.not_requires_symbols(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_not_requires_numbers_close():
    """Search IAM policy: Numbers requirement."""
    assert not iam.not_requires_numbers(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_numbers(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)
    with no_connection():
        assert not iam.not_requires_numbers(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_pass_len_unsafe_close():
    """Search IAM policy: Password length requirement."""
    assert not iam.min_password_len_unsafe(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY_BAD,
                                           retry=False)
    with no_connection():
        assert not iam.min_password_len_unsafe(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_pass_reuse_unsafe_close():
    """Search IAM policy: Password reuse requirement."""
    assert not iam.password_reuse_unsafe(AWS_ACCESS_KEY_ID,
                                         AWS_SECRET_ACCESS_KEY_BAD,
                                         retry=False)
    with no_connection():
        assert not iam.password_reuse_unsafe(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_pass_expiration_unsafe_close():
    """Search IAM policy: Password expiration requirement."""
    assert not iam.password_expiration_unsafe(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD,
                                              retry=False)
    with no_connection():
        assert not iam.password_expiration_unsafe(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_root_mfa_close():
    """Search IAM summary: MFA for root."""
    assert not iam.root_without_mfa(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY_BAD,
                                    retry=False)
    with no_connection():
        assert not iam.root_without_mfa(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_policies_attached_close():
    """Search IAM policies: Policies attached directly to users."""
    assert not iam.policies_attached_to_users(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD,
                                              retry=False)
    with no_connection():
        assert not iam.policies_attached_to_users(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_full_access_policies_close_1():
    """Search IAM policies: Full access policies."""
    assert not iam.have_full_access_policies(AWS_ACCESS_KEY_ID,
                                             AWS_SECRET_ACCESS_KEY)


def test_full_access_policies_close_2():
    """Search IAM policies: Full access policies."""
    assert not iam.have_full_access_policies(AWS_ACCESS_KEY_ID,
                                             AWS_SECRET_ACCESS_KEY_BAD,
                                             retry=False)


def test_full_access_policies_close_3():
    """Search IAM policies: Full access policies."""
    with no_connection():
        assert not iam.have_full_access_policies(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)


def test_not_support_role_close():
    """Search IAM policy: Support role."""
    assert not iam.has_not_support_role(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD,
                                        retry=False)
    with no_connection():
        assert not iam.has_not_support_role(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False)
