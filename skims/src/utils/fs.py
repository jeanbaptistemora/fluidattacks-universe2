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


async def recurse(path: str) -> Tuple[str, ...]:

    def _recurse(_path: str) -> Tuple[str, ...]:
        if os.path.isfile(_path):
            return (_path,)

        tree: Tuple[str, ...] = tuple(
            os.path.relpath(file)
            for entry in os.scandir(_path)
            for file in (
                _recurse(entry.path) if entry.is_dir() else [entry.path]
            )
        )

        return tree

    results: Tuple[str, ...] = await unblock(_recurse, path)

    return results


async def get_file_contents(path: str) -> str:
    async with aiofiles.open(
        path,
        mode='r',
        encoding='latin-1',
    ) as file_handle:
        file_contents: str = await file_handle.read()

        return file_contents
