# Standard library
import asyncio
import os
from typing import (
    Dict,
    List,
    Optional,
)


async def call(
    *cmd: List[str],
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stdin: int = asyncio.subprocess.DEVNULL,
    stdout: int = asyncio.subprocess.PIPE,
    stderr: int = asyncio.subprocess.PIPE,
    **kwargs,
) -> asyncio.subprocess.Process:
    return await asyncio.create_subprocess_exec(
        cmd[0], *cmd[1:],
        cwd=cwd,
        env={
            **os.environ.copy(),
            **(env or {}),
        },
        stderr=stderr,
        stdin=stdin,
        stdout=stdout,
    )
