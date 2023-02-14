import aioboto3
from aioboto3.dynamodb.table import (
    CustomTableResource,
)
from aiobotocore.config import (
    AioConfig,
)
from contextlib import (
    AsyncExitStack,
)
from ctx import (
    AWS_REGION_NAME,
)
from dynamodb.types import (
    Table,
)
from typing import (
    Any,
)

RESOURCE_OPTIONS = {
    "config": AioConfig(
        # The time in seconds till a timeout exception is thrown when
        # attempting to make a connection. [60]
        connect_timeout=15,
        # Maximum amount of simultaneously opened connections. [10]
        # https://docs.aiohttp.org/en/stable/client_advanced.html#limiting-connection-pool-size
        max_pool_connections=2000,
        # The time in seconds till a timeout exception is thrown when
        # attempting to read from a connection. [60]
        read_timeout=30,
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html
        retries={"max_attempts": 3, "mode": "standard"},
    ),
    "region_name": AWS_REGION_NAME,
    "service_name": "dynamodb",
    "use_ssl": True,
    "verify": True,
}
SESSION = aioboto3.Session()
CONTEXT_STACK = None
RESOURCE = None
TABLE_RESOURCES: dict[str, CustomTableResource] = {}


async def dynamo_startup() -> None:
    # pylint: disable=global-statement
    global CONTEXT_STACK, RESOURCE

    CONTEXT_STACK = AsyncExitStack()
    RESOURCE = await CONTEXT_STACK.enter_async_context(
        SESSION.resource(**RESOURCE_OPTIONS)
    )
    TABLE_RESOURCES["skims_sca"] = await RESOURCE.Table("skims_sca")


async def dynamo_shutdown() -> None:
    if CONTEXT_STACK:
        await CONTEXT_STACK.aclose()


async def get_resource() -> Any:
    if RESOURCE is None:
        await dynamo_startup()

    return RESOURCE


async def get_table_resource(table: Table) -> CustomTableResource:
    if table.name in TABLE_RESOURCES:
        return TABLE_RESOURCES[table.name]

    resource = await get_resource()
    return await resource.Table(table.name)
