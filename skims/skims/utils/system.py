# Standard library
import asyncio
import os
import subprocess  # nosec
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)


def blocking_call(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin: int = subprocess.DEVNULL,
    stdout: int = subprocess.PIPE,
    stderr: int = subprocess.PIPE,
    **kwargs: Any,
) -> subprocess.Popen:
    return subprocess.Popen(  # nosec
        [binary, *binary_args],
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

    return process


def blocking_read(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin_bytes: Optional[bytes] = None,
    stdout: int = subprocess.PIPE,
    stderr: int = subprocess.PIPE,
    **kwargs: Any,
) -> Tuple[int, bytes, bytes]:
    process = blocking_call(
        binary,
        *binary_args,
        cwd=cwd,
        env=env,
        stdin=(
            subprocess.DEVNULL
            if stdin_bytes is None
            else subprocess.PIPE
        ),
        stdout=stdout,
        stderr=stderr,
        **kwargs,
    )

    out, err = process.communicate(input=stdin_bytes)
    code = process.returncode

    return code, out, err


async def read(
    binary: str,
    *binary_args: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin_bytes: Optional[bytes] = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs: Any,
) -> Tuple[int, bytes, bytes]:
    process: asyncio.subprocess.Process = await call(
        binary,
        *binary_args,
        cwd=cwd,
        env=env,
        stdin=(
            asyncio.subprocess.DEVNULL
            if stdin_bytes is None
            else asyncio.subprocess.PIPE
        ),
        stdout=stdout,
        stderr=stderr,
        **kwargs,
    )

    out, err = await process.communicate(input=stdin_bytes)
    code = -1 if process.returncode is None else process.returncode

    return code, out, err
