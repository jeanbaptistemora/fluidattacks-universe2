# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from contextlib import (
    contextmanager,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_api")


from fluidasserts.cloud.aws import (
    s3,
)
from fluidasserts.helper import (
    aws,
)

# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Helpers
#


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


def _get_bucket_names(key_id: str, secret: str):
    buckets = aws.run_boto3_func(
        key_id=key_id,
        secret=secret,
        service="s3",
        func="list_buckets",
        param="Buckets",
    )
    return list(map(lambda x: x["Name"], buckets))


#
# Open tests
#


def test_bucket_logging_open():
    """Bucket has server access logging enabled?."""
    assert s3.has_server_access_logging_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    )


def test_public_buckets_open():
    """Check if account has public buckets."""
    assert s3.has_public_buckets(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def test_bucket_has_authenticated_access_open():
    """Check if account has buckets accesible to anyone authenticated."""
    assert s3.bucket_has_authenticated_access(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    )


def test_has_buckets_without_default_encryption_open():
    """Search S3 buckets without default encryption."""
    assert s3.has_buckets_without_default_encryption(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_buckets_allow_unauthorized_public_access_open():
    """Search for S3 buckets that allow unauthorized public access."""
    assert s3.buckets_allow_unauthorized_public_access(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_has_insecure_transport_open():
    """Search S3 cubes that use unsafe transport."""
    assert s3.has_insecure_transport(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_has_disabled_server_side_encryption_open():
    """Search S3 buckets with server side encryption disabled."""
    assert s3.has_disabled_server_side_encryption(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_bucket_objects_can_be_listed_open():
    """Search S3 buckets that can be listed."""
    assert s3.bucket_objects_can_be_listed(
        _get_bucket_names(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    ).is_open()


def test_buckets_has_permissive_acl_permissions_open():
    """Search S3 buckets with permissive ACL permissions."""
    assert s3.buckets_has_permissive_acl_permissions(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()


def test_bucket_has_object_lock_disabled_open():
    """Search S3 buckets with permissive ACL permissions."""
    assert s3.bucket_has_object_lock_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, bucket_name="df1test"
    ).is_open()


#
# Closing tests
#


def test_bucket_logging_close():
    """Bucket has server access logging enabled?."""
    assert not s3.has_server_access_logging_disabled(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False
    )
    with no_connection():
        assert not s3.has_server_access_logging_disabled(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False
        )


def test_public_buckets_close():
    """Check if account has public buckets."""
    assert not s3.has_public_buckets(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_BAD, retry=False
    )

    with no_connection():
        assert not s3.has_public_buckets(
            AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, retry=False
        )
