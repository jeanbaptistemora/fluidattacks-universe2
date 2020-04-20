# -*- coding: utf-8 -*-
# disable MyPy due to error "boto module has no attribute client, resource"
#  type: ignore

"""Functions to connect to dynamodb database."""

import os

import boto3

from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY, FI_AWS_DYNAMODB_SECRET_KEY, FI_ENVIRONMENT,
    FI_DYNAMODB_HOST, FI_DYNAMODB_PORT
)


RESOURCE_OPTIONS = {}
if FI_ENVIRONMENT == 'development' and FI_DYNAMODB_HOST:
    ENDPOINT_URL = 'http://{}:{}'.format(FI_DYNAMODB_HOST, FI_DYNAMODB_PORT)
    RESOURCE_OPTIONS = {
        'service_name': 'dynamodb',
        'aws_access_key_id': FI_AWS_DYNAMODB_ACCESS_KEY,
        'aws_secret_access_key': FI_AWS_DYNAMODB_SECRET_KEY,
        'aws_session_token': os.environ.get('AWS_SESSION_TOKEN'),
        'region_name': 'us-east-1',
        'endpoint_url': ENDPOINT_URL
    }
else:
    RESOURCE_OPTIONS = {
        'service_name': 'dynamodb',
        'aws_access_key_id': FI_AWS_DYNAMODB_ACCESS_KEY,
        'aws_secret_access_key': FI_AWS_DYNAMODB_SECRET_KEY,
        'aws_session_token': os.environ.get('AWS_SESSION_TOKEN'),
        'region_name': 'us-east-1'
    }

DYNAMODB_CLIENT = boto3.client(**RESOURCE_OPTIONS)
DYNAMODB_RESOURCE = boto3.resource(**RESOURCE_OPTIONS)
