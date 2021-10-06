import aioboto3
import botocore
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_DYNAMODB_HOST,
    FI_DYNAMODB_PORT,
    FI_ENVIRONMENT,
)
from contextlib import (
    asynccontextmanager,
)
from custom_exceptions import (
    UnavailabilityError,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
    DynamoQuery as DynamoQueryType,
)
from decimal import (
    Decimal,
)
import logging
import os
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

# Constants
LOGGER = logging.getLogger(__name__)
RESOURCE_OPTIONS: Dict[str, Optional[str]] = {
    "service_name": "dynamodb",
    "aws_access_key_id": FI_AWS_DYNAMODB_ACCESS_KEY,
    "aws_secret_access_key": FI_AWS_DYNAMODB_SECRET_KEY,
    "aws_session_token": os.environ.get("AWS_SESSION_TOKEN"),
    "region_name": "us-east-1",
    "config": botocore.config.Config(max_pool_connections=50),
}

if FI_ENVIRONMENT == "development" and FI_DYNAMODB_HOST:
    # FP: the endpoint is hosted in a local environment
    ENDPOINT_URL = f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}"  # NOSONAR
    RESOURCE_OPTIONS["endpoint_url"] = ENDPOINT_URL


@asynccontextmanager
async def client() -> aioboto3.session.Session.client:
    async with aioboto3.client(**RESOURCE_OPTIONS) as dynamodb_client:
        yield dynamodb_client


async def delete_item(table: str, delete_attrs: DynamoDeleteType) -> bool:
    success: bool = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.delete_item(**delete_attrs._asdict())
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


async def put_item(table: str, item: Dict[str, Any]) -> bool:
    success: bool = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.put_item(Item=item)
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


async def query(table: str, query_attrs: DynamoQueryType) -> List[Any]:
    response_items: List[Any]
    try:
        async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
            dynamo_table = await dynamodb_resource.Table(table)
            response = await dynamo_table.query(**query_attrs)
            response_items = response.get("Items", [])
            while response.get("LastEvaluatedKey"):
                query_attrs.update(
                    {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
                )
                response = await dynamo_table.query(**query_attrs)
                response_items += response.get("Items", [])
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return response_items


async def scan(table: str, scan_attrs: DynamoQueryType) -> List[Any]:
    response_items: List[Any]
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.scan(**scan_attrs)
        response_items = response.get("Items", [])
        while response.get("LastEvaluatedKey"):
            scan_attrs.update(
                {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
            )
            response = await dynamo_table.scan(**scan_attrs)
            response_items += response.get("Items", [])
    return response_items


def serialize(object_: Any) -> Any:
    """Convert an object so it can be serialized to dynamodb."""
    if isinstance(object_, (float, int)):
        object_ = Decimal(str(object_))
    elif isinstance(object_, dict):
        for key, value in object_.items():
            object_[key] = serialize(value)
    elif isinstance(object_, (list, set, tuple)):
        for value in object_:
            value = serialize(value)
    else:
        return object_
    return object_


@asynccontextmanager
async def start_context() -> aioboto3.session.Session.resource:
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        yield dynamodb_resource


async def update_item(table: str, update_attrs: Dict[str, Any]) -> bool:
    success: bool = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.update_item(**update_attrs)
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


def deserialize(object_: Any) -> Any:
    """Convert a Dynamo element so it can be serialized to json."""
    if isinstance(object_, Decimal):
        object_ = float(str(object_))
    elif isinstance(object_, dict):
        for key, value in object_.items():
            object_[key] = deserialize(value)
    elif isinstance(object_, (list, set, tuple)):
        for value in object_:
            value = deserialize(value)
    else:
        return object_
    return object_
