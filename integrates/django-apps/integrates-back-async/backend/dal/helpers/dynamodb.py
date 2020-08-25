# -*- coding: utf-8 -*-

"""Functions to connect to dynamodb database."""

import os
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

import logging
import aioboto3
import boto3
import botocore

from botocore.exceptions import ClientError
from backend.typing import (
    DynamoDelete as DynamoDeleteType,
    DynamoQuery as DynamoQueryType
)
from __init__ import (
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_ENVIRONMENT,
    FI_DYNAMODB_HOST, FI_DYNAMODB_PORT
)


# Constants
LOGGER = logging.getLogger(__name__)

CLIENT_CONFIG = botocore.config.Config(
    max_pool_connections=50,
)

RESOURCE_OPTIONS: Dict[str, Optional[str]] = {
    'service_name': 'dynamodb',
    'aws_access_key_id': FI_AWS_DYNAMODB_ACCESS_KEY,
    'aws_secret_access_key': FI_AWS_DYNAMODB_SECRET_KEY,
    'aws_session_token': os.environ.get('AWS_SESSION_TOKEN'),
    'region_name': 'us-east-1',
    'config': CLIENT_CONFIG
}

if FI_ENVIRONMENT == 'development' and FI_DYNAMODB_HOST:
    ENDPOINT_URL = 'http://{}:{}'.format(FI_DYNAMODB_HOST, FI_DYNAMODB_PORT)
    RESOURCE_OPTIONS['endpoint_url'] = ENDPOINT_URL

DYNAMODB_RESOURCE = boto3.resource(**RESOURCE_OPTIONS)
TABLE_NAME: str = 'integrates'


@asynccontextmanager
async def client() -> aioboto3.session.Session.client:
    async with aioboto3.client(**RESOURCE_OPTIONS) as dynamodb_client:
        yield dynamodb_client


async def async_delete_item(
        table: str,
        delete_attrs: DynamoDeleteType) -> bool:
    success: bool = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.delete_item(**delete_attrs._asdict())
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    return success


async def async_put_item(table: str, item: Dict[str, Any]) -> bool:
    success: bool = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.put_item(Item=item)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    return success


async def async_query(
        table: str, query_attrs: DynamoQueryType) -> List:
    response_items: List
    try:
        async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
            dynamo_table = await dynamodb_resource.Table(table)
            response = await dynamo_table.query(**query_attrs)
            response_items = response.get('Items', [])
            while response.get('LastEvaluatedKey'):
                query_attrs.update(
                    {'ExclusiveStartKey': response.get('LastEvaluatedKey')}
                )
                response = await dynamo_table.query(**query_attrs)
                response_items += response.get('Items', [])
    except ClientError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
        raise ex
    return response_items


async def async_scan(
        table: str, scan_attrs: DynamoQueryType) -> List:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.scan(**scan_attrs)
        response_items = response.get('Items', [])
        while response.get('LastEvaluatedKey'):
            scan_attrs.update(
                {'ExclusiveStartKey': response.get('LastEvaluatedKey')}
            )
            response = await dynamo_table.scan(**scan_attrs)
            response_items += response.get('Items', [])
    return response_items


async def async_update_item(
    table: str,
    update_attrs: Dict[str, Any]
) -> bool:
    success: bool = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.update_item(**update_attrs)
        success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    return success


@asynccontextmanager
async def start_context() -> aioboto3.session.Session.resource:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        yield dynamodb_resource
