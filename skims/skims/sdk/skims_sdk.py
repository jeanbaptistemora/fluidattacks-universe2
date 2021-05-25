# Standard library
import asyncio
import subprocess  # nosec
from os import (
    environ,
)
from typing import (
    List,
    Optional,
)

# Third party libraries
# None, NEVER, PLEASE !

# Local libraries
# None NEVER, PLEASE !


async def _run(*cmd: str, **env: str) -> bool:
    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        environ["SKIMS_BIN"],
        *cmd,
        env=env,
        stderr=None,
        stdin=subprocess.DEVNULL,
        stdout=None,
    )

    await process.wait()

    success: bool = process.returncode == 0

    return success


async def queue(
    finding_code: Optional[str],
    finding_title: Optional[str],
    group: str,
    urgent: bool,
    *,
    product_api_token: str,
) -> bool:
    cmd: List[str] = ["queue"]

    if finding_code:
        cmd.extend(["--finding-code", finding_code])

    if finding_title:
        cmd.extend(["--finding-title", finding_title])

    cmd.extend(["--group", group])

    if urgent:
        cmd.extend(["--urgent"])

    return await _run(*cmd, PRODUCT_API_TOKEN=product_api_token)
