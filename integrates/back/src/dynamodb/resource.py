import aioboto3
from aiobotocore.config import (
    AioConfig,
)
from context import (
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
    FI_DYNAMODB_HOST,
    FI_DYNAMODB_PORT,
    FI_ENVIRONMENT,
)
from contextlib import (
    AsyncExitStack,
)
from typing import (
    Any,
)

RESOURCE_OPTIONS = {
    "aws_access_key_id": FI_AWS_DYNAMODB_ACCESS_KEY,
    "aws_secret_access_key": FI_AWS_DYNAMODB_SECRET_KEY,
    "aws_session_token": FI_AWS_SESSION_TOKEN,
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
    ),
    "endpoint_url": (
        # FP: the endpoint is hosted in a local environment
        f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}"  # NOSONAR
        if FI_ENVIRONMENT == "development"
        else None
    ),
    "region_name": "us-east-1",
    "service_name": "dynamodb",
    "use_ssl": True,
    "verify": True,
}
SESSION = aioboto3.Session()
CONTEXT_STACK = None
RESOURCE = None


async def dynamo_startup() -> None:
    # pylint: disable=global-statement
    global CONTEXT_STACK, RESOURCE

    stack = AsyncExitStack()
    RESOURCE = await stack.enter_async_context(
        SESSION.resource(**RESOURCE_OPTIONS)
    )
    CONTEXT_STACK = stack


async def dynamo_shutdown() -> None:
    if CONTEXT_STACK:
        await CONTEXT_STACK.aclose()


async def get_resource() -> Any:
    if RESOURCE is None:
        await dynamo_startup()

    return RESOURCE
