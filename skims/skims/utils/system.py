# Standard library
import asyncio
import os
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)


async def call(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin: Optional[int] = None,
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

    return process


async def read(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin: Optional[int] = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs: Any,
) -> Tuple[int, bytes, bytes]:
    process: asyncio.subprocess.Process = await call(
        binary,
        *binary_args,
        cwd=cwd,
        env=env,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        **kwargs,
    )

    out, err = await process.communicate()
    code = -1 if process.returncode is None else process.returncode

    return code, out, err
