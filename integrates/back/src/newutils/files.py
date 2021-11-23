from aioextensions import (
    in_thread,
)
from binaryornot.check import (
    is_binary,
)
import magic
import os
from starlette.concurrency import (
    run_in_threadpool,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    List,
)


def assert_file_mime(filename: str, allowed_mimes: List[str]) -> bool:
    mime_type = magic.from_file(filename, mime=True)
    return mime_type in allowed_mimes


async def assert_uploaded_file_mime(
    file_instance: UploadFile, allowed_mimes: List[str]
) -> bool:
    mime_type = await get_uploaded_file_mime(file_instance)
    return mime_type in allowed_mimes


async def get_file_size(file_object: UploadFile) -> int:
    file = file_object.file

    # Needed while upstream starlette implements a size method
    # pylint: disable=protected-access
    if file_object._in_memory:
        current_position = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(current_position)
    else:
        current_position = await run_in_threadpool(file.tell)
        await run_in_threadpool(file.seek, 0, os.SEEK_END)
        size = await run_in_threadpool(file.tell)
        await run_in_threadpool(file.seek, current_position)
    return size


async def get_uploaded_file_mime(file_instance: UploadFile) -> str:
    mime_type: str = magic.from_buffer(await file_instance.read(), mime=True)
    await file_instance.seek(0)
    return mime_type


async def get_lines_count(filename: str) -> int:
    """Get the number of lines in a file if is non binary."""
    if not await in_thread(is_binary, filename):
        return await in_thread(_get_num_lines, filename)
    return 0


def _get_num_lines(filename: str) -> int:
    with open(filename, encoding="latin-1") as content:
        num_lines = len(content.readlines())
    return num_lines
