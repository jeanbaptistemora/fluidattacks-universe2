#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""Lambda function."""

import boto3
import json


def lambda_handler(event, context):
    """Secure function."""
    client = boto3.client("iam")
    user = event["user"]

    response = client.get_user(UserName=user)
    return json.dumps(response, default=str)
