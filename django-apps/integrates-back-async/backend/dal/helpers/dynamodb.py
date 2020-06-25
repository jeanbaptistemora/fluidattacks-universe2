# -*- coding: utf-8 -*-

"""Functions to connect to dynamodb database."""

import os
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

import aioboto3
import boto3
import botocore

from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_ENVIRONMENT,
    FI_DYNAMODB_HOST, FI_DYNAMODB_PORT
)


CLIENT_CONFIG = botocore.config.Config(
    max_pool_connections=30,
)
RESOURCE_OPTIONS: Dict[str, Optional[str]] = {}

if FI_ENVIRONMENT == 'development' and FI_DYNAMODB_HOST:
    ENDPOINT_URL = 'http://{}:{}'.format(FI_DYNAMODB_HOST, FI_DYNAMODB_PORT)
    RESOURCE_OPTIONS = {
        'service_name': 'dynamodb',
        'aws_access_key_id': FI_AWS_DYNAMODB_ACCESS_KEY,
        'aws_secret_access_key': FI_AWS_DYNAMODB_SECRET_KEY,
        'aws_session_token': os.environ.get('AWS_SESSION_TOKEN'),
        'region_name': 'us-east-1',
        'config': CLIENT_CONFIG,
        'endpoint_url': ENDPOINT_URL
    }
else:
    RESOURCE_OPTIONS = {
        'service_name': 'dynamodb',
        'aws_access_key_id': FI_AWS_DYNAMODB_ACCESS_KEY,
        'aws_secret_access_key': FI_AWS_DYNAMODB_SECRET_KEY,
        'aws_session_token': os.environ.get('AWS_SESSION_TOKEN'),
        'region_name': 'us-east-1',
        'config': CLIENT_CONFIG
    }

DYNAMODB_RESOURCE = boto3.resource(**RESOURCE_OPTIONS)
TABLE_NAME: str = 'integrates'


async def async_put_item(table: str, item: Dict[str, Any]) -> None:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        await dynamo_table.put_item(Item=item)


async def async_query(table: str, query_attrs: Dict[str, str]) -> \
        List[Dict[str, Any]]:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.query(**query_attrs)
        response_items = response.get('Items', [])
    return response_items


@asynccontextmanager
async def start_context() -> aioboto3.session.Session.resource:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        yield dynamodb_resource
