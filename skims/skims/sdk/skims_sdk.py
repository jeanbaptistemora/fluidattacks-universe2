import aioboto3
import asyncio
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from enum import (
    Enum,
)
import json
import os
from os import (
    environ,
)
import subprocess  # nosec
from typing import (
    Any,
    Dict,
    Optional,
    Set,
    Tuple,
)

HOLIDAYS: Set[str] = {
    # Colombia, next five years
    "21-01-01",
    "21-01-11",
    "21-03-22",
    "21-04-01",
    "21-04-02",
    "21-05-01",
    "21-05-17",
    "21-06-07",
    "21-06-14",
    "21-07-05",
    "21-07-20",
    "21-08-07",
    "21-08-16",
    "21-10-18",
    "21-11-01",
    "21-11-15",
    "21-12-08",
    "21-12-25",
    "22-01-10",
    "22-03-21",
    "22-04-14",
    "22-04-15",
    "22-05-01",
    "22-05-30",
    "22-06-20",
    "22-06-27",
    "22-07-04",
    "22-07-20",
    "22-08-07",
    "22-08-15",
    "22-10-17",
    "22-11-07",
    "22-11-14",
    "22-12-08",
    "22-12-25",
    "23-01-09",
    "23-03-20",
    "23-04-06",
    "23-04-07",
    "23-05-01",
    "23-05-22",
    "23-06-12",
    "23-06-19",
    "23-07-03",
    "23-07-20",
    "23-08-07",
    "23-08-21",
    "23-10-16",
    "23-11-06",
    "23-11-13",
    "23-12-08",
    "23-12-25",
    "24-01-01",
    "24-01-08",
    "24-03-25",
    "24-03-28",
    "24-03-29",
    "24-05-01",
    "24-05-13",
    "24-06-03",
    "24-06-10",
    "24-07-01",
    "24-08-07",
    "24-08-19",
    "24-10-14",
    "24-11-04",
    "24-11-11",
    "24-12-25",
    "25-01-01",
    "25-01-06",
    "25-03-24",
    "25-04-17",
    "25-04-18",
    "25-05-01",
    "25-06-02",
    "25-06-23",
    "25-06-30",
    "25-08-07",
    "25-08-18",
    "25-10-13",
    "25-11-03",
    "25-11-17",
    "25-12-08",
    "25-12-25",
}


class AvailabilityEnum(Enum):
    ALWAYS: str = "ALWAYS"
    NEVER: str = "NEVER"
    WORKING_HOURS: str = "WORKING_HOURS"

    def is_available_right_now(self) -> bool:
        now: datetime = datetime.now(timezone(timedelta(hours=-5)))  # Colombia

        if self == AvailabilityEnum.ALWAYS:
            return True
        if self == AvailabilityEnum.NEVER:
            return False
        if self == AvailabilityEnum.WORKING_HOURS:
            in_working_days: bool = 0 <= now.weekday() <= 5  # Monday to Friday
            in_working_hours: bool = 9 <= now.hour < 16  # [9:00, 15:59] Col
            is_holiday: bool = now.strftime("%y-%m-%d") in HOLIDAYS
            return in_working_days and in_working_hours and not is_holiday

        raise NotImplementedError()


def _json_load(path: str) -> Any:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


FINDINGS: Dict[str, Dict[str, Dict[str, str]]] = _json_load(
    environ["SKIMS_FINDINGS"]
)
QUEUES: Dict[str, Dict[str, str]] = _json_load(environ["SKIMS_QUEUES"])


def get_available_queues() -> Dict[str, Dict[str, str]]:
    return {
        queue: data
        for queue, data in QUEUES.items()
        if AvailabilityEnum(data["availability"]).is_available_right_now()
    }


def is_check_available(finding_code: str) -> bool:
    for data in QUEUES.values():
        if finding_code in data["findings"]:
            return AvailabilityEnum(
                data["availability"]
            ).is_available_right_now()

    raise NotImplementedError(f"{finding_code} does not belong to a queue")


def print_available_queues() -> None:
    print(json.dumps(get_available_queues(), indent=2, sort_keys=True))


async def _run(
    cmd: str,
    *cmd_args: str,
    stderr: Optional[int] = None,
    stdout: Optional[int] = None,
    **env: str,
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    final_env = environ.copy()
    final_env.update(env)

    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        cmd,
        *cmd_args,
        env=final_env,
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
        str(urgent).lower(),
        PRODUCT_API_TOKEN=product_api_token,
        stderr=stderr,
        stdout=stdout,
        MAKES_COMPUTE_ON_AWS_BATCH_QUEUE=get_queue_for_finding(
            finding_code,
            urgent=urgent,
        ),
    )


async def queue_boto3(
    finding_code: str,
    group: str,
    namespace: str,
    urgent: bool,
) -> Dict[str, Any]:
    queue_name = get_queue_for_finding(finding_code, urgent=urgent)
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_ACCESS_KEY_ID"],
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
    )
    async with aioboto3.client(**resource_options) as batch:
        return await batch.submit_job(
            jobName=f"process-{group}-{finding_code}-{namespace}",
            jobQueue=queue_name,
            jobDefinition="makes",
            containerOverrides={
                "vcpus": 1,
                "command": [
                    "m",
                    "f",
                    "/skims/process-group",
                    group,
                    finding_code,
                    namespace,
                ],
                "environment": [
                    {"name": "CI", "value": "true"},
                    {"name": "MAKES_AWS_BATCH_COMPAT", "value": "true"},
                    {
                        "name": "PRODUCT_API_TOKEN",
                        "value": os.environ.get("PRODUCT_API_TOKEN"),
                    },
                ],
                "memory": 1 * 1800,
            },
            retryStrategy={
                "attempts": 1,
            },
            timeout={"attemptDurationSeconds": 86400},
        )
