# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    run,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
from s3.resource import (
    s3_shutdown,
    s3_startup,
)
from schedulers.report_machine import (
    process_execution,
)
from server import (
    SERVER,
)


async def wrap(execution_id: str) -> None:
    await dynamo_startup()
    await s3_startup()
    try:
        await process_execution(execution_id)
    finally:
        await dynamo_shutdown()
        await s3_shutdown()


@SERVER.task(serializer="json", name="process-machine-result")
def report(execution_id: str) -> None:
    run(wrap(execution_id))
