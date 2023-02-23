import aioboto3
from botocore.exceptions import (
    ClientError,
)
from contextlib import (
    asynccontextmanager,
)
from custom_exceptions import (
    UnavailabilityError,
)
from decimal import (
    Decimal,
)
from dynamodb.resource import (
    get_resource,
    RESOURCE_OPTIONS,
    SESSION,
)
import logging
from typing import (
    Any,
    NamedTuple,
)

# Constants
LOGGER = logging.getLogger(__name__)


class DynamoDelete(NamedTuple):
    Key: dict[str, Any]


@asynccontextmanager
async def client() -> aioboto3.session.Session.client:
    async with SESSION.client(**RESOURCE_OPTIONS) as dynamodb_client:
        yield dynamodb_client


async def delete_item(table: str, delete_attrs: DynamoDelete) -> bool:
    success: bool = False
    dynamodb_resource = await get_resource()
    dynamo_table = await dynamodb_resource.Table(table)
    response = await dynamo_table.delete_item(**delete_attrs._asdict())
    success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


async def put_item(table: str, item: dict[str, Any]) -> bool:
    success: bool = False
    dynamodb_resource = await get_resource()
    dynamo_table = await dynamodb_resource.Table(table)
    response = await dynamo_table.put_item(Item=item)
    success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


async def query(table: str, query_attrs: dict[str, Any]) -> list[Any]:
    response_items: list[Any]
    try:
        dynamodb_resource = await get_resource()
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.query(**query_attrs)
        response_items = response.get("Items", [])
        while response.get("LastEvaluatedKey") and (
            not query_attrs.get("Limit")
            or len(response_items) < int(query_attrs["Limit"])
        ):
            query_attrs.update(
                {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
            )
            response = await dynamo_table.query(**query_attrs)
            response_items += response.get("Items", [])
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return response_items


async def get_item(table: str, query_attrs: dict[str, Any]) -> dict[str, Any]:
    response_items: dict[str, Any]
    try:
        dynamodb_resource = await get_resource()
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.get_item(**query_attrs)
        response_items = response.get("Item", {})
    except ClientError as ex:
        raise UnavailabilityError() from ex
    return response_items


async def scan(table: str, scan_attrs: dict[str, Any]) -> list[Any]:
    response_items: list[Any]
    dynamodb_resource = await get_resource()
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


async def update_item(table: str, update_attrs: dict[str, Any]) -> bool:
    success: bool = False
    dynamodb_resource = await get_resource()
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
