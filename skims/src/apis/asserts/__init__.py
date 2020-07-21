# Standard library
import asyncio
import contextlib
import os
from tempfile import NamedTemporaryFile
from textwrap import dedent
from typing import (
    Iterator,
    IO,
)

# Local libraries
from utils.system import (
    call,
)


@contextlib.contextmanager
def create_exploit_blocking(content: str) -> Iterator[IO[bytes]]:
    with NamedTemporaryFile() as file:
        file.write(dedent(content).encode())
        file.seek(0)

        yield file


async def execute(content: str) -> asyncio.subprocess.Process:
    asserts: str = os.environ.get('BIN_ASSERTS', 'asserts')

    with create_exploit_blocking(content) as exploit:
        process: asyncio.subprocess.Process = await call(
            asserts, '--no-color', exploit.name,
        )

        await process.wait()

        return process
