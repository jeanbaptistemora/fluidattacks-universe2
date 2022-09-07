# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Test methods of fluidasserts.helper.http."""


import os
import pytest

pytestmark = pytest.mark.asserts_module("helper")


from fluidasserts.helper import (
    aws,
)


def test_policy_statement_privilege():
    """test iam._policy_statements_privilege."""
    assert not aws.policy_statement_privilege(
        {
            "Effect": "Allow",
            "Action": ["rds:DescribeAccountAttributes"],
            "Resource": "*",
        },
        "Allow",
        "write",
    )
    assert not aws.policy_statement_privilege(
        {
            "Effect": "Allow",
            "Action": ["rds:DescribeAccountAttributes*"],
            "Resource": "*",
        },
        "Allow",
        "write",
    )
    assert aws.policy_statement_privilege(
        {
            "Effect": "Allow",
            "Action": ["rds:*AccountAttributes"],
            "Resource": "*",
        },
        "Allow",
        "write",
    )
