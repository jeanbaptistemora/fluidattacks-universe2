# Standard library
from itertools import (
    chain,
)
from operator import (
    attrgetter,
    methodcaller,
)
import os
from typing import (
    AsyncGenerator,
    Tuple,
)

# Third party imports
import aiofiles

# Local libraries
from utils.aio import (
    materialize,
)


async def generate_file_content(path: str) -> AsyncGenerator[str, None]:
    file_contents: str = await get_file_content(path)

    while True:
        yield file_contents


async def generate_file_raw_content(path: str) -> AsyncGenerator[bytes, None]:
    file_contents: bytes = await get_file_raw_content(path)

    while True:
        yield file_contents


async def get_file_content(path: str, encoding: str = 'latin-1') -> str:
    async with aiofiles.open(
        path,
        mode='r',
        encoding=encoding,
    ) as file_handle:
        file_contents: str = await file_handle.read()

        return file_contents


async def get_file_raw_content(path: str) -> bytes:
    async with aiofiles.open(path, mode='rb') as file_handle:
        file_contents: bytes = await file_handle.read()

        return file_contents


async def recurse_dir(path: str) -> Tuple[str, ...]:
    scanner = tuple(os.scandir(path))

    dirs = map(attrgetter('path'), filter(methodcaller('is_dir'), scanner))
    files = map(attrgetter('path'), filter(methodcaller('is_file'), scanner))

    tree: Tuple[str, ...] = tuple(chain(
        files, *await materialize(map(recurse_dir, dirs)),
    ))

    return tree


async def recurse(path: str) -> Tuple[str, ...]:
    return (path,) if os.path.isfile(path) else await recurse_dir(path)
