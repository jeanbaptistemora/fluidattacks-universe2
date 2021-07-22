import asyncio
import json
from os import (
    environ,
)
import subprocess  # nosec
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)


def _json_load(path: str) -> Any:
    with open(path) as file:
        return json.load(file)


FINDINGS: Dict[str, Dict[str, Dict[str, str]]] = _json_load(
    environ["SKIMS_FINDINGS"]
)
QUEUES: Dict[str, List[str]] = _json_load(environ["SKIMS_QUEUES"])


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
    namespace: str,
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
    cmd.extend(["--namespace", namespace])

    if urgent:
        cmd.extend(["--urgent"])

    return await _run(
        *cmd,
        PRODUCT_API_TOKEN=product_api_token,
        stderr=stderr,
        stdout=stdout,
    )
