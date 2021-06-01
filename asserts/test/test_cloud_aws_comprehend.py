# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.cloud packages."""


from contextlib import (
    contextmanager,
)
import os
import pytest

pytestmark = pytest.mark.asserts_module("cloud_aws_api")


from fluidasserts.cloud.aws import (
    comprehend,
)

# Constants
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY_BAD = "bad"


#
# Open tests
#


def test_eno_encryption_on_analysis_job_open():
    """Check if Comprehend jobs have their output encrypted."""
    assert comprehend.no_encryption_on_analysis_job(
        AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    ).is_open()
