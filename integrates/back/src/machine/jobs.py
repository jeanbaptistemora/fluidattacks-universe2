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
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    PRODUCT_API_TOKEN,
)
from contextlib import (
    suppress,
)
import datetime
from dateutil.parser import (  # type: ignore
    parse as date_parse,
)
from db_model.roots.get import (
    get_machine_executions_by_job_id,
)
from db_model.roots.types import (
    GitRootItem,
    LastMachineExecutions,
    MachineFindingResult,
    RootMachineExecutionItem,
)
from enum import (
    Enum,
)
import json
import logging
import logging.config
import more_itertools
from more_itertools import (
    collapse,
)
from newutils import (
    datetime as datetime_utils,
)
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


def _get_jobs_that_have_no_logs(
    jobs_details_from_batch: Dict[str, Dict[str, Any]],
    not_allowed_jobs_ids: List[str],
) -> List[Job]:
    jobs: List[Job] = []
    for job_id, job_item in jobs_details_from_batch.items():
        if job_id in not_allowed_jobs_ids:
            continue
        group = job_item["container"]["command"][3]
        for git_root_nickname in json.loads(
            job_item["container"]["command"][5]
        ):
            jobs.append(
                Job(
                    created_at=job_item.get("createdAt"),
                    exit_code=job_item.get("container", {}).get("exitCode"),
                    exit_reason=job_item.get("container", {}).get("reason"),
                    id=job_item["jobId"],
                    name=f"skims-process-{group}-{git_root_nickname}",
                    root_nickname=git_root_nickname,
                    queue=job_item["jobQueue"].split("/")[-1],
                    started_at=job_item.get("startedAt", 0),
                    stopped_at=job_item.get("stoppedAt", 0),
                    status=job_item["status"],
                )
            )
    return jobs


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

    jobs_details_from_batch = {
        item["jobId"]: item
        for item in (await describe_jobs(*list_jobs_from_batch.keys()))
        if finding_code in json.loads(item["container"]["command"][-2])
        and item["status"] in {x.name for x in statuses}
    }
    job_logs_description = await list_log_streams(group_name)

    job_items = []
    jobs_listed: List[str] = []

    root_machine_executions: Dict[str, Dict[str, RootMachineExecutionItem]] = {
        job_id: {execution.root_id: execution for execution in executions}
        for job_id, executions in await collect(
            _get_machine_executions_by_job_id(
                job_id=job_id,
            )
            for job_id in list_jobs_from_batch.keys()
        )
    }
    for job_item in job_logs_description:
        group, job_id, git_root_nickname = job_item["logStreamName"].split("/")
        jobs_listed.append(job_id)
        if job_id not in jobs_details_from_batch:
            continue

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

        job_items.append(
            Job(
                created_at=jobs_details_from_batch[job_id].get("createdAt"),
                exit_code=jobs_details_from_batch[job_id]
                .get("container", {})
                .get("exitCode"),
                exit_reason=jobs_details_from_batch[job_id]
                .get("container", {})
                .get("reason"),
                id=jobs_details_from_batch[job_id]["jobId"],
                name=f"skims-process-{group}-{git_root_nickname}",
                root_nickname=job_item["logStreamName"].split("/")[-1],
                queue=jobs_details_from_batch[job_id]["jobQueue"].split("/")[
                    -1
                ],
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
                status=jobs_details_from_batch[job_id]["status"],
                vulnerabilities=vulns_summary,
            )
        )
    job_items.extend(
        _get_jobs_that_have_no_logs(
            jobs_details_from_batch=jobs_details_from_batch,
            not_allowed_jobs_ids=jobs_listed,
        )
    )
    return sorted(
        job_items,
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
    **kwargs: Any,
) -> Dict[str, Any]:
    queue_name = "skims_all_soon"
    job_name = f"skims-process-{group}-{finding_code}"
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.Session().client(**resource_options) as batch:
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
                "vcpus": 4 if len(namespaces) >= 4 else len(namespaces),
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
            **kwargs,
        )


def _get_seconds_ago(timestamp: int) -> float:
    date = datetime.datetime.fromtimestamp(int(timestamp / 1000))
    now = datetime.datetime.utcnow()
    return (now - date).seconds


async def queue_all_checks_new(
    group: str,
    finding_codes: Tuple[str, ...],
    queue: SkimsBatchQueue,
    roots: Optional[Tuple[str, ...]] = None,
) -> Dict[str, Any]:
    queue_name = queue.value
    job_name = f"skims-process-{group}"
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.Session().client(**resource_options) as batch:
        current_jobs = [
            job
            for job in (
                await list_jobs_filter(queue=queue_name, filters=(job_name,))
            )["jobSummaryList"]
            if job["status"]
            in {
                "SUBMITTED",
                "PENDING",
                "RUNNABLE",
                "STARTING",
                "RUNNING",
            }
        ]
        jobs_description = (
            [
                job
                for job in await describe_jobs(
                    *[job["jobId"] for job in current_jobs]
                )
                if job["status"] != "RUNNING"
                or (
                    job["status"] == "RUNNING"
                    and "startedAt" in job
                    and (_get_seconds_ago(job["startedAt"]) / 60) <= 5
                    # jobs that have been running for four minutes are still
                    # installing makes
                )
            ]
            if current_jobs
            else ()
        )
        roots_to_execute = set(
            collapse(
                [
                    json.loads(job["container"]["command"][5])
                    for job in jobs_description
                    if len(job["container"]["command"]) == 6
                ],
                base_type=str,
            )
        )
        findings_to_execute = set(
            collapse(
                [
                    json.loads(job["container"]["command"][4])
                    for job in jobs_description
                ],
                base_type=str,
            )
        )

        if (roots and tuple(roots_to_execute)) == roots and (
            tuple(findings_to_execute) == finding_codes
        ):
            return {"error": "The job is already running"}

        if roots:
            roots = tuple(set((*roots, *roots_to_execute)))
        finding_codes = tuple(set((*finding_codes, *findings_to_execute)))

        for job in jobs_description:
            with suppress(ClientError):
                await batch.cancel_job(
                    jobId=job["jobId"],
                    reason="another job was queued",
                )
            with suppress(ClientError):
                await batch.terminate_job(
                    jobId=job["jobId"],
                    reason="another job was queued",
                )
        envars = [
            {"name": "CI", "value": "true"},
            {"name": "MAKES_AWS_BATCH_COMPAT", "value": "true"},
            {
                "name": "PRODUCT_API_TOKEN",
                "value": PRODUCT_API_TOKEN,
            },
        ]
        command = [
            "m",
            "f",
            "/skims/process-group-all",
            group,
            json.dumps(list(finding_codes)),
        ]
        if not roots:
            envars.append(
                {"name": "MACHINE_ALL_ROOTS", "value": "true"},
            )
        else:
            command.append(json.dumps(list(roots)))
        return await batch.submit_job(
            jobName=job_name,
            jobQueue=queue_name,
            jobDefinition="makes",
            containerOverrides={
                "vcpus": 4,
                "command": command,
                "environment": envars,
                "memory": 1 * 1800,
            },
            retryStrategy={
                "attempts": 1,
            },
            timeout={"attemptDurationSeconds": 86400},
        )


async def get_active_executions(root: GitRootItem) -> LastMachineExecutions:
    group: str = root.group_name
    complete_jobs_response = await collect(
        list_jobs_filter(
            queue=queue.value,
            filters=(f"skims-process-{group}",),
            maxResults=1,
        )
        for queue in SkimsBatchQueue
    )
    specific_jobs_response = await list_jobs_filter(
        queue=SkimsBatchQueue.HIGH.value,
        filters=(f"skims-process-{group}-*",),
        maxResults=1,
    )
    active_complete_jobs: List[
        Tuple[Dict[str, Any], SkimsBatchQueue]
    ] = sorted(
        [
            (response["jobSummaryList"][0], queue)
            for response, queue in zip(complete_jobs_response, SkimsBatchQueue)
            if "jobSummaryList" in response
            and response["jobSummaryList"]
            and response["jobSummaryList"][0]["status"]
            not in {"FAILED", "SUCCEEDED"}
        ],
        key=lambda x: x[0]["createdAt"],
        reverse=True,
    )
    active_specific_job: Optional[Dict[str, Any]] = (
        specific_jobs_response["jobSummaryList"][0]
        if "jobSummaryList" in specific_jobs_response
        and specific_jobs_response["jobSummaryList"]
        and specific_jobs_response["jobSummaryList"][0]["status"]
        not in {"FAILED", "SUCCEEDED"}
        else None
    )
    if active_specific_job:
        specific_job_description = await describe_jobs(
            active_specific_job["jobId"]
        )
    return LastMachineExecutions(
        complete=RootMachineExecutionItem(
            job_id=active_complete_jobs[0][0]["jobId"],
            created_at=datetime_utils.get_from_epoch(
                active_complete_jobs[0][0]["createdAt"] / 1000
            ),
            started_at=datetime_utils.get_from_epoch(
                active_complete_jobs[0][0]["startedAt"] / 1000
            )
            if active_complete_jobs[0][0].get("startedAt")
            else None,
            stopped_at=datetime_utils.get_from_epoch(
                active_complete_jobs[0][0]["stoppedAt"] / 1000
            )
            if active_complete_jobs[0][0].get("stoppedAt")
            else None,
            name=active_complete_jobs[0][0]["jobName"],
            findings_executed=[
                MachineFindingResult(open=0, modified=0, finding=fin)
                for fin in FINDINGS.keys()
            ],
            queue=active_complete_jobs[0][1].value,
            root_id=root.id,
        )
        if active_complete_jobs
        else None,
        specific=RootMachineExecutionItem(
            job_id=active_specific_job["jobId"],
            created_at=datetime_utils.get_from_epoch(
                active_specific_job["createdAt"] / 1000
            ),
            started_at=datetime_utils.get_from_epoch(
                active_specific_job["startedAt"] / 1000
            )
            if active_specific_job.get("startedAt")
            else None,
            stopped_at=datetime_utils.get_from_epoch(
                active_specific_job["stoppedAt"] / 1000
            )
            if active_specific_job.get("stoppedAt")
            else None,
            name=active_specific_job["jobName"],
            findings_executed=[
                MachineFindingResult(
                    open=0,
                    modified=0,
                    finding=active_specific_job["jobName"].split("-")[-1],
                )
            ],
            queue=SkimsBatchQueue.HIGH.value,
            root_id=root.id,
        )
        if active_specific_job
        and root.state.nickname
        in specific_job_description[0]["container"]["command"][-1]
        else None,
    )
