# Standard library
import os
from typing import (
    Tuple,
)

# Third party imports
import aiofiles

# Local libraries
from utils.aio import (
    unblock,
)


def recurse_blocking(path: str) -> Tuple[str, ...]:
    if os.path.isfile(path):
        return (path,)

    tree: Tuple[str, ...] = tuple(
        os.path.relpath(file)
        for entry in os.scandir(path)
        for file in (
            recurse_blocking(entry.path) if entry.is_dir() else [entry.path]
        )
    )

    return tree


async def recurse(path: str) -> Tuple[str, ...]:
    results: Tuple[str, ...] = await unblock(recurse_blocking, path)

    return results


async def file_as_lines(file: str) -> Tuple[Tuple[int, str], ...]:
    async with aiofiles.open(
        file,
        mode='r',
        encoding='latin-1',
    ) as file_handle:
        file_contents: str = await file_handle.read()

        return tuple(enumerate(file_contents.splitlines(), start=1))
