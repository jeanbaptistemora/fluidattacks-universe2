import asyncio
from datetime import (
    datetime,
    timezone,
)
from enum import (
    Enum,
)
import json
from os import (
    environ,
)
import subprocess  # nosec
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)


class AvailabilityEnum(Enum):
    ALWAYS: str = "ALWAYS"
    NEVER: str = "NEVER"
    WORKING_HOURS: str = "WORKING_HOURS"

    def is_available_right_now(self) -> bool:
        now: datetime = datetime.now(timezone.utc)

        if self == AvailabilityEnum.ALWAYS:
            return True
        if self == AvailabilityEnum.NEVER:
            return False
        if self == AvailabilityEnum.WORKING_HOURS:
            in_working_days: bool = 0 <= now.weekday() <= 5  # Monday to Friday
            in_working_hours: bool = 14 <= now.hour <= 21  # 9am to 5pm Col
            is_holiday: bool = False
            return in_working_days and in_working_hours and not is_holiday

        raise NotImplementedError()


def _json_load(path: str) -> Any:
    with open(path) as file:
        return json.load(file)


FINDINGS: Dict[str, Dict[str, Dict[str, str]]] = _json_load(
    environ["SKIMS_FINDINGS"]
)
QUEUES: Dict[str, Dict[str, str]] = _json_load(environ["SKIMS_QUEUES"])


async def _run(
    cmd: str,
    *cmd_args: str,
    stderr: Optional[int] = None,
    stdout: Optional[int] = None,
    **env: str,
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        cmd,
        *cmd_args,
        env=env,
        stderr=stderr,
        stdin=subprocess.DEVNULL,
        stdout=stdout,
    )

    out, err = await process.communicate()
    code = -1 if process.returncode is None else process.returncode

    return code, out, err


def get_finding_code_from_title(finding_title: str) -> Optional[str]:
    for finding_code in FINDINGS:
        for locale in FINDINGS[finding_code]:
            if finding_title == FINDINGS[finding_code][locale]["title"]:
                return finding_code
    return None


def get_priority_suffix(urgent: bool) -> str:
    return "soon" if urgent else "later"


def get_queue_for_finding(finding_code: str, urgent: bool = False) -> str:
    for queue_ in QUEUES:
        if finding_code in QUEUES[queue_]["findings"]:
            return f"{queue_}_{get_priority_suffix(urgent)}"

    raise NotImplementedError(f"{finding_code} does not belong to a queue")


async def queue(
    finding_code: str,
    group: str,
    namespace: str,
    urgent: bool,
    *,
    product_api_token: str,
    stderr: Optional[int] = None,
    stdout: Optional[int] = None,
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    return await _run(
        environ["SKIMS_PROCESS_GROUP_ON_AWS"],
        group,
        finding_code,
        namespace,
        PRODUCT_API_TOKEN=product_api_token,
        stderr=stderr,
        stdout=stdout,
        MAKES_COMPUTE_ON_AWS_JOB_QUEUE=get_queue_for_finding(
            finding_code,
            urgent=urgent,
        ),
    )
