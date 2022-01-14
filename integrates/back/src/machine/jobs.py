import aioboto3
from aioextensions import (
    collect,
)
from batch.dal import (
    describe_jobs,
    Job,
    JobStatus,
    list_jobs_by_group,
    list_jobs_filter,
    list_log_streams,
)
from batch.types import (
    VulnerabilitiesSummary,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    PRODUCT_API_TOKEN,
)
from dateutil.parser import (  # type: ignore
    parse as date_parse,
)
from db_model.roots.get import (
    get_machine_executions_by_job_id,
)
from db_model.roots.types import (
    RootMachineExecutionItem,
)
from enum import (
    Enum,
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


class SkimsBatchQueue(Enum):
    HIGH: str = "skims_all_soon"
    LOW: str = "skims_all_later"


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


async def _get_machine_executions_by_job_id(
    *, job_id: str, root_id: Optional[str] = None
) -> Tuple[str, Tuple[RootMachineExecutionItem, ...]]:
    return (
        job_id,
        await get_machine_executions_by_job_id(job_id=job_id, root_id=root_id),
    )


async def list_(  # pylint: disable=too-many-locals
    *,
    finding_code: str,
    group_name: str,
    include_non_urgent: bool = False,
    include_urgent: bool = False,
    statuses: List[JobStatus],
    group_roots: Dict[str, str],
) -> List[Job]:
    list_jobs_from_batch: Dict[str, Dict[str, Any]] = {
        item["jobId"]: item
        for item in more_itertools.flatten(
            [
                await list_jobs_by_group(_queue, group_name)
                for _queue in [
                    *(["skims_all_later"] if include_non_urgent else []),
                    *(["skims_all_soon"] if include_urgent else []),
                ]
            ]
        )
    }

    jobs_details = {
        item["jobId"]: item
        for item in (await describe_jobs(*list_jobs_from_batch.keys()))
        if finding_code in json.loads(item["container"]["command"][-2])
        and item["status"] in {x.name for x in statuses}
    }

    job_logs_description = await list_log_streams(
        group_name, *jobs_details.keys()
    )

    root_machine_executions: Dict[str, Dict[str, RootMachineExecutionItem]] = {
        job_id: {execution.root_id: execution for execution in executions}
        for job_id, executions in await collect(
            _get_machine_executions_by_job_id(
                job_id=job_id,
            )
            for job_id in list_jobs_from_batch.keys()
        )
    }

    jobs = []

    for job_item in job_logs_description:
        group, job_id, git_root_nickname = job_item["logStreamName"].split("/")

        db_execution: Optional[RootMachineExecutionItem] = None
        vulns_summary: Optional[RootMachineExecutionItem] = None

        if git_root_nickname in group_roots:
            db_execution = root_machine_executions.get(job_id, {}).get(
                group_roots[git_root_nickname]
            )
            if db_execution and (
                _vulns := [
                    x
                    for x in db_execution.findings_executed
                    if x.finding == finding_code
                ]
            ):
                vulns_summary = VulnerabilitiesSummary(
                    modified=_vulns[0].modified, open=_vulns[0].open
                )

        jobs.append(
            Job(
                created_at=jobs_details[job_id].get("createdAt"),
                exit_code=jobs_details[job_id]
                .get("container", {})
                .get("exitCode"),
                exit_reason=jobs_details[job_id]
                .get("container", {})
                .get("reason"),
                id=jobs_details[job_id]["jobId"],
                name=f"skims-process-{group}-{git_root_nickname}",
                root_nickname=job_item["logStreamName"].split("/")[-1],
                queue=jobs_details[job_id]["jobQueue"].split("/")[-1],
                started_at=int(
                    date_parse(db_execution.started_at).timestamp() * 1000
                )
                if db_execution
                else job_item.get("firstEventTimestamp", 0),
                stopped_at=int(
                    date_parse(db_execution.stopped_at).timestamp() * 1000
                )
                if db_execution
                else job_item.get("lastEventTimestamp", 0),
                status=jobs_details[job_id]["status"],
                vulnerabilities=vulns_summary,
            )
        )

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
    namespaces: Tuple[str, ...],
) -> Dict[str, Any]:
    queue_name = "skims_all_soon"
    job_name = f"skims-process-{group}-{finding_code}"
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.client(**resource_options) as batch:
        current_jobs = await list_jobs_filter(
            queue=queue_name, filters=(job_name,), maxResults=1
        )
        if len(current_jobs["jobSummaryList"]) > 0:
            current_job = current_jobs["jobSummaryList"][0]

            if current_job["status"] in {
                "SUBMITTED",
                "PENDING",
                "RUNNABLE",
                "STARTING",
                "RUNNING",
            }:
                current_job_description = (
                    await describe_jobs(current_job["jobId"])
                )[0]
                roots_to_execute = json.loads(
                    current_job_description["container"]["command"][-1]
                )
                if tuple(roots_to_execute) == namespaces:
                    return {"error": "The job is already running"}
                if current_job["status"] in {
                    "STARTING",
                    "RUNNING",
                }:
                    # only run the roots that are not in the current job
                    namespaces = tuple(
                        set(namespaces).difference(set(roots_to_execute))
                    )
                else:
                    # cancel the queued job and create a new one by
                    # joining the roots
                    namespaces = tuple(set((*namespaces, *roots_to_execute)))
                    await batch.cancel_job(
                        jobId=current_job["jobId"],
                        reason="another job was queued",
                    )

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
                    json.dumps(list(namespaces)),
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
    roots: Tuple[str, ...],
    finding_codes: Tuple[str, ...],
    queue: SkimsBatchQueue,
) -> Dict[str, Any]:
    queue_name = queue.value
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
                    json.dumps(list(finding_codes)),
                    json.dumps(list(roots)),
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
