# Standard library
import asyncio
import contextlib
import json
import os
from tempfile import NamedTemporaryFile
from textwrap import dedent
from typing import (
    Dict,
    Iterator,
    IO,
    Optional,
    Tuple,
)

# Local libraries
from utils.logs import (
    log_blocking,
)
from utils.system import (
    call,
)


@contextlib.contextmanager
def create_exploit_blocking(
    content: str,
    args: Optional[Dict[str, str]] = None,
) -> Iterator[IO[bytes]]:
    args = args or {}

    boostrap: str = f"""
        ARGS = json.loads(
            bytes.fromhex('{json.dumps(args).encode().hex()}').decode()
        )
    """

    with NamedTemporaryFile() as file:
        exploit: str = '\n'.join(map(dedent, [boostrap, content]))

        file.write(exploit.encode())
        file.seek(0)

        log_blocking('debug', 'Exploit: %s \nArgs: %s', exploit, args)

        yield file


async def execute(content: str) -> asyncio.subprocess.Process:
    asserts: str = os.environ.get('BIN_ASSERTS', 'asserts')

    with create_exploit_blocking(content) as exploit:
        process: asyncio.subprocess.Process = await call(
            asserts, '--no-color', exploit.name,
        )

        return process


async def get_vulnerabilities(content: str) -> Tuple[str, ...]:
    process: asyncio.subprocess.Process = await execute(content)

    vulnerabilities: Tuple[str, ...]

    if process.returncode == 0:
        # Pending to add parser here
        vulnerabilities = ()
    else:
        vulnerabilities = ()

    return vulnerabilities
