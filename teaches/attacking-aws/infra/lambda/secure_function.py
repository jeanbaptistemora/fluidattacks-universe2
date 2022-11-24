#!/usr/bin/env python3

"""Lambda function."""

import boto3
import json


def lambda_handler(event, context):
    """Secure function."""
    client = boto3.client("iam")
    user = event["user"]

    response = client.get_user(UserName=user)
    return json.dumps(response, default=str)
