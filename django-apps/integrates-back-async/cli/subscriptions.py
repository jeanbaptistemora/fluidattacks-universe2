# Standard library
import asyncio
import importlib
import sys


async def main():
    module, func = sys.argv[1].rsplit('.', maxsplit=1)
    await getattr(importlib.import_module(module), func)()


if __name__ == '__main__':
    asyncio.run(main())
