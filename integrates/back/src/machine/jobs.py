import aioboto3
from batch.dal import (
    describe_jobs,
    Job,
    JobStatus,
    list_jobs_by_group,
    list_jobs_filter,
    list_log_streams,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    PRODUCT_API_TOKEN,
)
import json
import logging
import logging.config
import more_itertools
import os
from settings.logger import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)


def _json_load(path: str) -> Any:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
QUEUES: Dict[str, Dict[str, str]] = _json_load(os.environ["MACHINE_QUEUES"])
FINDINGS: Dict[str, Dict[str, Dict[str, str]]] = _json_load(
    os.environ["MACHINE_FINDINGS"]
)


class JobArguments(NamedTuple):
    group_name: str
    finding_code: str
    root_nickname: str


def parse_name(name: str) -> JobArguments:
    tokens = name.split("-", maxsplit=3)
    return JobArguments(
        finding_code=tokens[2],
        group_name=tokens[1],
        root_nickname=tokens[3],
    )


def _get_priority_suffix(urgent: bool) -> str:
    return "soon" if urgent else "later"


def get_queue_for_finding(finding_code: str, urgent: bool = False) -> str:
    for queue_ in QUEUES:
        if finding_code in QUEUES[queue_]["findings"]:
            return f"{queue_}_{_get_priority_suffix(urgent)}"

    raise NotImplementedError(f"{finding_code} does not belong to a queue")


def get_finding_code_from_title(finding_title: str) -> Optional[str]:
    for finding_code in FINDINGS:
        for locale in FINDINGS[finding_code]:
            if finding_title == FINDINGS[finding_code][locale]["title"]:
                return finding_code
    return None


async def list_(
    *,
    finding_code: str,
    group_name: str,
    include_non_urgent: bool = False,
    include_urgent: bool = False,
    statuses: List[JobStatus],
) -> List[Job]:
    queues: List[str] = []
    if include_non_urgent:
        queues.append("skims_all_later")
    if include_urgent:
        queues.append("skims_all_soon")

    list_jobs: Dict[str, Dict[str, Any]] = {
        item["jobId"]: item
        for item in more_itertools.flatten(
            [await list_jobs_by_group(_queue, group_name) for _queue in queues]
        )
    }

    job_items = {
        item["jobId"]: item
        for item in (await describe_jobs(*list_jobs.keys()))
        if finding_code in json.loads(item["container"]["command"][-2])
        and item["status"] in {x.name for x in statuses}
    }

    job_logs: Dict[str, Dict[str, Any]] = {
        item["logStreamName"].split("/")[1]: item
        for item in await list_log_streams(group_name, *job_items.keys())
    }

    jobs = [
        Job(
            created_at=job_items[job_id].get("createdAt"),
            exit_code=job_items[job_id].get("container", {}).get("exitCode"),
            exit_reason=job_items[job_id].get("container", {}).get("reason"),
            id=job_items[job_id]["jobId"],
            name=job_items[job_id]["jobName"],
            root_nickname=job_logs[job_id]["logStreamName"].split("/")[-1],
            queue=job_items[job_id]["jobQueue"],
            started_at=job_logs[job_id].get("firstEventTimestamp", 0),
            stopped_at=job_logs[job_id].get("lastEventTimestamp", 0),
            status=job_items[job_id]["status"],
        )
        for job_id in job_logs.keys()
    ]

    return sorted(
        jobs,
        key=lambda job: job.created_at or 0,
        reverse=True,
    )


async def _list_jobs_by_name(
    queue: str, status: JobStatus, filters: Tuple[str, ...]
) -> List[Job]:
    next_token = "dummy"  # nosec
    jobs = []
    while next_token:
        response = await list_jobs_filter(
            queue=queue,
            filters=filters,
            **(
                {"next_token": next_token}
                if next_token and next_token != "dummy"  # nosec
                else {}
            ),
        )
        next_token = response.get("nexToken", None)
        jobs.extend(
            [
                Job(
                    created_at=job_summary.get("createdAt"),
                    exit_code=job_summary.get("container", {}).get("exitCode"),
                    exit_reason=job_summary.get("container", {}).get("reason"),
                    id=job_summary["jobId"],
                    name=job_summary["jobName"],
                    queue=queue,
                    started_at=job_summary.get("startedAt"),
                    stopped_at=job_summary.get("stoppedAt"),
                    status=job_summary["status"],
                )
                for job_summary in response.get("jobSummaryList", [])
                if job_summary["status"] == status.name
            ]
        )
    return jobs


async def queue_boto3(
    group: str,
    finding_code: str,
    namespace: str,
) -> Dict[str, Any]:
    queue_name = "skims_all_soon"
    job_name = f"skims-process-{group}-{finding_code}-{namespace}"
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.client(**resource_options) as batch:
        return await batch.submit_job(
            jobName=job_name,
            jobQueue=queue_name,
            jobDefinition="makes",
            containerOverrides={
                "vcpus": 1,
                "command": [
                    "m",
                    "f",
                    "/skims/process-group-all",
                    group,
                    json.dumps([finding_code]),
                    json.dumps([namespace]),
                ],
                "environment": [
                    {"name": "CI", "value": "true"},
                    {"name": "MAKES_AWS_BATCH_COMPAT", "value": "true"},
                    {
                        "name": "PRODUCT_API_TOKEN",
                        "value": PRODUCT_API_TOKEN,
                    },
                ],
                "memory": 1 * 1800,
            },
            retryStrategy={
                "attempts": 1,
            },
            timeout={"attemptDurationSeconds": 86400},
        )


async def queue_all_checks_new(
    group: str,
    roots: List[str],
    finding_codes: List[str],
) -> Dict[str, Any]:
    queue_name = "skims_all_later"
    job_name = f"skims-process-{group}"
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.client(**resource_options) as batch:
        return await batch.submit_job(
            jobName=job_name,
            jobQueue=queue_name,
            jobDefinition="makes",
            containerOverrides={
                "vcpus": 4 if len(roots) >= 4 else len(roots),
                "command": [
                    "m",
                    "f",
                    "/skims/process-group-all",
                    group,
                    json.dumps(finding_codes),
                    json.dumps(roots),
                ],
                "environment": [
                    {"name": "CI", "value": "true"},
                    {"name": "MAKES_AWS_BATCH_COMPAT", "value": "true"},
                    {
                        "name": "PRODUCT_API_TOKEN",
                        "value": PRODUCT_API_TOKEN,
                    },
                ],
                "memory": 1 * 1800,
            },
            retryStrategy={
                "attempts": 1,
            },
            timeout={"attemptDurationSeconds": 86400},
        )
