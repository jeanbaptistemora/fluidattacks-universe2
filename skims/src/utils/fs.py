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
    Awaitable,
    Callable,
    Dict,
    Tuple,
)

# Third party imports
import aiofiles
from aioextensions import (
    collect,
)

# Local libraries
from utils.function import (
    locked,
)


def generate_file_content(path: str) -> Callable[[], Awaitable[str]]:
    data: Dict[str, str] = {}

    @locked
    async def get_one() -> str:
        if not data:
            data['file_contents'] = await get_file_content(path)
        return data['file_contents']

    return get_one


def generate_file_raw_content(path: str) -> Callable[[], Awaitable[bytes]]:
    data: Dict[str, bytes] = {}

    @locked
    async def get_one() -> bytes:
        if not data:
            data['file_raw_content'] = await get_file_raw_content(path)
        return data['file_raw_content']

    return get_one


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
        files, *await collect(map(recurse_dir, dirs)),
    ))

    return tree


async def recurse(path: str) -> Tuple[str, ...]:
    return (path,) if os.path.isfile(path) else await recurse_dir(path)
