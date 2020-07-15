# Standard library
import asyncio
import importlib
import sys
from asgiref.sync import sync_to_async


async def main():
    module, func = sys.argv[1].rsplit('.', maxsplit=1)
    to_invoke = getattr(importlib.import_module(module), func)
    if asyncio.iscoroutinefunction(to_invoke):
        await to_invoke()
    else:
        await sync_to_async(to_invoke)()


if __name__ == '__main__':
    asyncio.run(main())
