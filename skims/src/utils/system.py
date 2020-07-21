# Standard library
import asyncio
import os
from typing import (
    Any,
    Dict,
    Optional,
)


async def call(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin: int = asyncio.subprocess.DEVNULL,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs: Any,
) -> asyncio.subprocess.Process:
    process = await asyncio.create_subprocess_exec(
        binary,
        *binary_args,
        cwd=cwd,
        env={
            **os.environ.copy(),
            **(env or {}),
        },
        stderr=stderr,
        stdin=stdin,
        stdout=stdout,
        **kwargs,
    )

    await process.wait()

    return process
