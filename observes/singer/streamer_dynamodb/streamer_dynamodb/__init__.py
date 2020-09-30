# Standard Library
import argparse
import asyncio
import json
import time
from decimal import Decimal
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Optional,
    TypeVar,
)

# Third Library
import aioboto3
import botocore
from aioextensions import in_thread
from aiomultiprocess import Pool

# Local imports
from streamer_dynamodb.logs import LOGGER

# Constants
CLIENT_CONFIG = botocore.config.Config(max_pool_connections=50)

# Constants
TVar = TypeVar('TVar')


async def scan_table(
    table_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region_name: str,
    **kwargs: str,
) -> AsyncGenerator[Dict[str, Any], None]:
    """Return an dynamodb result generator.

    :param table_name: Name of dynamodb table.
    :param connection: A dynamodb connection.
    :yield: DynamoDb scan result.
    :rtype: Generator[Dict, None, None].
    """
    resource_options: Dict[str, Optional[str]] = {
        'service_name': 'dynamodb',
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'region_name': region_name,
        'config': CLIENT_CONFIG,
        **kwargs
    }
    scan_params = {'TableName': table_name, 'Limit': 1000}

    async with aioboto3.resource(**resource_options) as dynamodb_resource:
        table = await dynamodb_resource.Table(table_name)
        has_more = True
        result = {}
        retries = 0

        while has_more:
            try:
                result = await table.scan(**scan_params)
                retries = 0
                for item in result.get('Items', []):
                    yield item
            except botocore.exceptions.ClientError as exc:
                if exc.response['Error'][
                        'Code'] == 'ResourceNotFoundException':
                    LOGGER.error("Failed to scan table %s", table_name)
                    LOGGER.error("Exception: %s", str(exc))
                    has_more = False
                    continue
                if retries > 4:
                    LOGGER.error("Failed to scan table %s", table_name)
                    LOGGER.error("Exception: %s", str(exc))
                    has_more = False
                    continue
                time.sleep(5)
                LOGGER.warning("Trying to scan the table %s", table_name)
                retries += 1
                continue

            if result.get('LastEvaluatedKey', None):
                scan_params['ExclusiveStartKey'] = result.get(
                    'LastEvaluatedKey')

            has_more = result.get('LastEvaluatedKey', False)


async def dump_table(connection_args: Dict[str, str]) -> str:
    table_name = connection_args.pop('table_name')
    LOGGER.info("Scanning %s", table_name)

    lock = asyncio.Lock()
    async for item in scan_table(table_name, **connection_args):
        item = deserialize(item)
        record: str = await in_thread(json.dumps, {
            "stream": table_name,
            "record": item
        })
        async with lock:
            print(record)
    return table_name


def deserialize(object_: Any) -> Any:
    """Convert an object so it can be serialized to JSON.

    :param object_: Object to deserialize.
    :return: A deserialized object.
    :rtype: Any.
    """
    if isinstance(object_, Decimal):
        object_ = float(object_)
    elif isinstance(object_, dict):
        object_ = {key: deserialize(value) for key, value in object_.items()}
    elif isinstance(object_, (list)):
        object_ = [deserialize(value) for value in object_]
    elif isinstance(object_, set):
        object_ = [deserialize(value) for value in object_]
    elif isinstance(object_, tuple):
        object_ = [deserialize(value) for value in object_]
    else:
        return object_
    return object_


async def _main() -> None:
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--auth',
                        help='JSON authentication file',
                        dest='auth',
                        type=argparse.FileType('r'),
                        required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c',
                       '--conf',
                       help='JSON config file',
                       dest='conf',
                       type=argparse.FileType('r'))
    args = parser.parse_args()

    credentials: Dict[str, str] = json.load(args.auth)
    configuration = json.load(args.conf)

    aws_access_key_id = credentials.pop('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = credentials.pop('AWS_SECRET_ACCESS_KEY')
    region_name = credentials.pop('AWS_DEFAULT_REGION')
    async with Pool() as pool:
        async for result in pool.map(dump_table, [
                dict(table_name=table,
                     aws_access_key_id=aws_access_key_id,
                     aws_secret_access_key=aws_secret_access_key,
                     region_name=region_name)
                for table in configuration.get("tables", [])
        ]):
            LOGGER.info("Success dump table: %s", result)


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
