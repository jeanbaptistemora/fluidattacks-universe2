# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import aioboto3
from aiobotocore.config import (
    AioConfig,
)
from botocore import (
    UNSIGNED,
)
from contextlib import (
    AsyncExitStack,
)
from ctx import (
    AWS_REGION_NAME,
)
from typing import (
    Any,
)

RESOURCE_OPTIONS = {
    "config": AioConfig(
        connect_timeout=15,
        max_pool_connections=2000,
        read_timeout=30,
        retries={"max_attempts": 10, "mode": "standard"},
        signature_version="s3v4",
    ),
    "region_name": AWS_REGION_NAME,
    "service_name": "s3",
    "use_ssl": True,
    "verify": True,
}
PUBLIC_RESOURCE_OPTIONS = {
    "config": AioConfig(
        connect_timeout=15,
        max_pool_connections=2000,
        read_timeout=30,
        retries={"max_attempts": 10, "mode": "standard"},
        signature_version=UNSIGNED,
    ),
    "region_name": AWS_REGION_NAME,
    "service_name": "s3",
    "use_ssl": True,
    "verify": True,
}
SESSION = aioboto3.Session()
CONTEXT_STACK = None
RESOURCE = None


async def s3_startup(is_public: bool) -> None:
    # pylint: disable=global-statement
    global CONTEXT_STACK, RESOURCE

    CONTEXT_STACK = AsyncExitStack()

    RESOURCE = await CONTEXT_STACK.enter_async_context(
        SESSION.client(
            **(PUBLIC_RESOURCE_OPTIONS if is_public else RESOURCE_OPTIONS)
        )
    )


async def s3_shutdown() -> None:
    if CONTEXT_STACK:
        await CONTEXT_STACK.aclose()


async def get_s3_resource(*, is_public: bool = False) -> Any:
    if RESOURCE is None:
        await s3_startup(is_public)

    return RESOURCE
