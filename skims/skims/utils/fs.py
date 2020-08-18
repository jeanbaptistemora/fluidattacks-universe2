# Standard library
from itertools import (
    chain,
)
from operator import (
    attrgetter,
    methodcaller,
)
import os
from shutil import (
    rmtree,
)
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
    in_thread,
    in_process,
)

# Local libraries
from utils.function import (
    never_concurrent,
)


def generate_file_content(
    path: str,
    encoding: str = 'latin-1',
    size: int = -1,
) -> Callable[[], Awaitable[str]]:
    data: Dict[str, str] = {}

    @never_concurrent
    async def get_one() -> str:
        if not data:
            data['file_contents'] = await get_file_content(
                path=path,
                encoding=encoding,
                size=size,
            )
        return data['file_contents']

    return get_one


def generate_file_raw_content(
    path: str,
    size: int = -1,
) -> Callable[[], Awaitable[bytes]]:
    data: Dict[str, bytes] = {}

    @never_concurrent
    async def get_one() -> bytes:
        if not data:
            data['file_raw_content'] = await get_file_raw_content(path, size)
        return data['file_raw_content']

    return get_one


async def get_file_content(
    path: str,
    encoding: str = 'latin-1',
    size: int = -1,
) -> str:
    async with aiofiles.open(
        path,
        mode='r',
        encoding=encoding,
    ) as file_handle:
        file_contents: str = await file_handle.read(size)

        return file_contents


async def get_file_raw_content(path: str, size: int = -1) -> bytes:
    async with aiofiles.open(path, mode='rb') as file_handle:
        file_contents: bytes = await file_handle.read(size)

        return file_contents


async def mkdir(name: str, mode: int = 0o777, exist_ok: bool = False) -> None:
    return await in_thread(os.makedirs, name, mode=mode, exist_ok=exist_ok)


async def rmdir(name: str) -> None:
    return await in_process(rmtree, name)


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
