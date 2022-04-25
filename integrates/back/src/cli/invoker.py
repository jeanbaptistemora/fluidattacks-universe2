from aioextensions import (
    in_thread,
    run,
)
import asyncio
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
import importlib
import sys


async def main() -> None:
    module, func = sys.argv[1].rsplit(".", maxsplit=1)
    to_invoke = getattr(importlib.import_module(module), func)
    await dynamo_startup()
    try:
        if asyncio.iscoroutinefunction(to_invoke):
            await to_invoke()
        else:
            await in_thread(
                to_invoke,
            )
    finally:
        await dynamo_shutdown()


if __name__ == "__main__":
    run(main())
