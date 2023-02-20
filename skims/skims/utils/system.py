import asyncio
from datetime import (
    datetime,
)
import os
import psutil
import subprocess  # nosec
import time
from typing import (
    Any,
)


def call_blocking(
    binary: str,
    *binary_args: str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
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
    cwd: str | None = None,
    env: dict[str, str] | None = None,
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


def read_blocking(
    binary: str,
    *binary_args: str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    stdin_bytes: bytes | None = None,
    stdout: int = subprocess.PIPE,
    stderr: int = subprocess.PIPE,
    **kwargs: Any,
) -> tuple[int, bytes, bytes]:
    process = call_blocking(
        binary,
        *binary_args,
        cwd=cwd,
        env=env,
        stdin=(subprocess.DEVNULL if stdin_bytes is None else subprocess.PIPE),
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
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    stdin_bytes: bytes | None = None,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs: Any,
) -> tuple[int, bytes, bytes]:
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


def wait_until_memory_usage(
    percent: float,
    timeout: float | None = None,
    interval: float | None = None,
) -> None:
    interval = interval or 0.01
    current_date = datetime.now()
    while psutil.virtual_memory().percent > percent:
        if timeout:
            elapsed_time = current_date - datetime.now()
            if elapsed_time.seconds > timeout:
                raise TimeoutError()
        time.sleep(interval)
