# Standard library
import os
from typing import (
    AsyncGenerator,
    Dict,
    Tuple,
)

# Third party imports
import aiofiles

# Local libraries
from utils.aio import (
    unblock,
)


async def generate_file_content(path: str) -> AsyncGenerator[str, None]:
    file_contents: str = await get_file_content(path)

    while True:
        yield file_contents


async def get_char_to_line_mapping(
    *,
    lines: Tuple[str, ...],
) -> Dict[int, int]:

    def _get_char_to_line_mapping() -> Dict[int, int]:
        mapping: Dict[int, int] = {}

        # Add 1 to take into account for the new line
        lines_length: Tuple[int, ...] = tuple(len(line) + 1 for line in lines)

        line: int = 0
        for char_number in range(0, sum(lines_length) + 1):
            mapping[char_number] = line + 1

            if char_number == lines_length[line]:
                line += 1

        return mapping

    return await unblock(_get_char_to_line_mapping)


async def get_file_content(path: str) -> str:
    async with aiofiles.open(
        path,
        mode='r',
        encoding='latin-1',
    ) as file_handle:
        file_contents: str = await file_handle.read()

        return file_contents


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
