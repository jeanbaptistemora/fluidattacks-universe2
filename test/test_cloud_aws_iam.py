# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""

# standard imports
import os

# 3rd party imports
# None

# local imports
from fluidasserts.cloud.aws import iam


# Constants
AWS_ACCESS_KEY_ID="AKIAIHT6LQIROIL7LKYQ"
AWS_SECRET_ACCESS_KEY="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"
AWS_SECRET_ACCESS_KEY_BAD="bad"

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

#
# Closing tests
#

def test_has_mfa_disabled_close():
    """Search MFA on IAM users."""
    assert not iam.has_mfa_disabled(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY)
    assert not iam.has_mfa_disabled(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.has_mfa_disabled(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_have_old_creds_enabled_close():
    """Search old unused passwords."""
    assert not iam.have_old_creds_enabled(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    assert not iam.have_old_creds_enabled(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.have_old_creds_enabled(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_have_old_access_keys_close():
    """Search old access keys."""
    assert not iam.have_old_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.have_old_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.have_old_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_root_has_access_keys_close():
    """Search root access keys."""
    assert not iam.root_has_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.root_has_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.root_has_access_keys(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_not_requires_uppercase_close():
    """Search IAM policy: Uppercase letter requirement."""
    assert not iam.not_requires_uppercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_uppercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.not_requires_uppercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_not_requires_lowercase_close():
    """Search IAM policy: Lowercase letter requirement."""
    assert not iam.not_requires_lowercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_lowercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.not_requires_lowercase(AWS_ACCESS_KEY_ID,
                                          AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_not_requires_symbols_close():
    """Search IAM policy: Symbols requirement."""
    assert not iam.not_requires_symbols(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_symbols(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.not_requires_symbols(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_not_requires_numbers_close():
    """Search IAM policy: Numbers requirement."""
    assert not iam.not_requires_numbers(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    assert not iam.not_requires_numbers(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.not_requires_numbers(AWS_ACCESS_KEY_ID,
                                        AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_pass_len_unsafe_close():
    """Search IAM policy: Password length requirement."""
    assert not iam.min_password_len_unsafe(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.min_password_len_unsafe(AWS_ACCESS_KEY_ID,
                                           AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_pass_reuse_unsafe_close():
    """Search IAM policy: Password reuse requirement."""
    assert not iam.password_reuse_unsafe(AWS_ACCESS_KEY_ID,
                                         AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.password_reuse_unsafe(AWS_ACCESS_KEY_ID,
                                         AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_pass_expiration_unsafe_close():
    """Search IAM policy: Password expiration requirement."""
    assert not iam.password_expiration_unsafe(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.password_expiration_unsafe(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_root_mfa_close():
    """Search IAM summary: MFA for root."""
    assert not iam.root_without_mfa(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.root_without_mfa(AWS_ACCESS_KEY_ID,
                                    AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)


def test_policies_attached_close():
    """Search IAM policies: Policies attached directly to users."""
    assert not iam.policies_attached_to_users(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY)
    assert not iam.policies_attached_to_users(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY_BAD)

    os.environ['http_proxy'] = 'https://0.0.0.0:8080'
    os.environ['https_proxy'] = 'https://0.0.0.0:8080'

    assert not iam.policies_attached_to_users(AWS_ACCESS_KEY_ID,
                                              AWS_SECRET_ACCESS_KEY)
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)
