"""Test methods of fluidasserts.cloud.cloudformation.elb2 module."""


from contextlib import (
    contextmanager,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_api")


from fluidasserts.cloud.aws import (
    elb2,
)

# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


@contextmanager
def no_connection():
    """Proxy something temporarily."""
    os.environ["HTTP_PROXY"] = "127.0.0.1:8080"
    os.environ["HTTPS_PROXY"] = "127.0.0.1:8080"
    try:
        yield
    finally:
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)


def test_has_access_logging_disabled_open():
    """Test elb2.has_access_logging_disabled."""
    assert elb2.has_access_logging_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_listeners_not_using_https_open():
    """Test elb2.listener_not_using_https."""
    assert elb2.listeners_not_using_https(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_uses_insecure_ssl_protocol_open():
    """Test elb2.uses_insecure_ssl_protocol."""
    assert elb2.uses_insecure_ssl_protocol(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_uses_insecure_ssl_cipher_open():
    """Test elb2.uses_insecure_ssl_cipher."""
    assert elb2.uses_insecure_ssl_cipher(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_uses_insecure_security_policy_open():
    """Test elb2.uses_insecure_security_policy."""
    assert elb2.uses_insecure_security_policy(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_has_not_deletion_protection_unknown():
    """Test elb2.has_not_deletion_protection."""
    with no_connection():
        assert elb2.has_not_deletion_protection(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False
        ).is_unknown()


def test_has_access_logging_disabled_unknown():
    """Test elb2.has_access_logging_disabled."""
    with no_connection():
        assert elb2.has_access_logging_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False
        ).is_unknown()
