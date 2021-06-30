import asyncio
from os import (
    environ,
)
import subprocess  # nosec
from typing import (
    List,
    Optional,
    Set,
    Tuple,
)


async def _run(
    *cmd: str,
    stderr: Optional[int] = None,
    stdout: Optional[int] = None,
    **env: str,
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        environ["SKIMS_BIN"],
        *cmd,
        env=env,
        stderr=stderr,
        stdin=subprocess.DEVNULL,
        stdout=stdout,
    )

    out, err = await process.communicate()
    code = -1 if process.returncode is None else process.returncode

    return code, out, err


async def queue(
    finding_code: Optional[str],
    finding_title: Optional[str],
    group: str,
    roots: Set[str],  # pylint: disable=unused-argument
    urgent: bool,
    *,
    product_api_token: str,
    stderr: Optional[int] = None,
    stdout: Optional[int] = None,
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    cmd: List[str] = ["queue"]

    if finding_code:
        cmd.extend(["--finding-code", finding_code])

    if finding_title:
        cmd.extend(["--finding-title", finding_title])

    cmd.extend(["--group", group])

    if urgent:
        cmd.extend(["--urgent"])

    return await _run(
        *cmd,
        PRODUCT_API_TOKEN=product_api_token,
        stderr=stderr,
        stdout=stdout,
    )
