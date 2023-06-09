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
from server import (
    SERVER,
)
from server.report_machine import (
    process_execution,
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
