# Standard library
import asyncio
import importlib
import sys

from aioextensions import (
    in_thread,
    run,
)


async def main():
    module, func = sys.argv[1].rsplit('.', maxsplit=1)
    to_invoke = getattr(importlib.import_module(module), func)
    if asyncio.iscoroutinefunction(to_invoke):
        await to_invoke()
    else:
        await in_thread(to_invoke,)


if __name__ == '__main__':
    run(main())
