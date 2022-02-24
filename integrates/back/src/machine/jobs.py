import aioboto3
from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    describe_jobs,
    get_actions_by_name,
    Job,
    JobStatus,
    list_jobs,
    list_jobs_by_status,
    list_log_streams,
    put_action,
)
from batch.types import (
    VulnerabilitiesSummary,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
)
import datetime
from dateutil.parser import (  # type: ignore
    parse as date_parse,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.get import (
    get_machine_executions,
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
    Union,
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
    jobs_runnable_from_batch: Dict[str, Dict[str, Any]] = {
        item["jobId"]: item
        for item in more_itertools.flatten(
            await collect(
                (
                    list_jobs_by_status(_queue, status=status)
                    for _queue in [
                        *(["skims_all_later"] if include_non_urgent else []),
                        *(["skims_all_soon"] if include_urgent else []),
                    ]
                    for status in (x.name for x in statuses)
                )
            )
        )
        if item["jobName"].startswith == f"skims-process-{group_name}"
    }
    jobs_details_from_batch = {
        item["jobId"]: item
        for item in (await describe_jobs(*jobs_runnable_from_batch.keys()))
        if finding_code in json.loads(item["container"]["command"][4])
        and item["status"] in {x.name for x in statuses}
    }
    jobs_from_db: Tuple[RootMachineExecutionItem, ...] = tuple(
        execution
        for execution in collapse(
            (
                await collect(
                    get_machine_executions(root_id=root_id)
                    for root_id in group_roots.keys()
                )
            ),
            base_type=RootMachineExecutionItem,
        )
        if any(
            find.finding == finding_code
            for find in execution.findings_executed
        )
    )

    job_items = []
    jobs_listed: List[str] = []

    for job_execution in jobs_from_db:
        jobs_listed.append(job_execution.job_id)
        _vulns = [
            x
            for x in job_execution.findings_executed
            if x.finding == finding_code
        ]
        job_items.append(
            Job(
                created_at=job_execution.created_at,
                exit_code=0,
                exit_reason="",
                id=job_execution.job_id,
                name=job_execution.name,
                root_nickname=group_roots[job_execution.root_id],
                queue=job_execution.queue,
                started_at=int(
                    date_parse(job_execution.started_at).timestamp() * 1000
                ),
                stopped_at=int(
                    date_parse(job_execution.stopped_at).timestamp() * 1000
                ),
                status="SUCCESS" if job_execution.success else "FAILED",
                vulnerabilities=VulnerabilitiesSummary(
                    modified=_vulns[0].modified, open=_vulns[0].open
                ),
            )
        )
    job_logs_description = (
        await list_log_streams(group_name, *jobs_runnable_from_batch.keys())
        if len(jobs_runnable_from_batch.keys()) > 0
        else []
    )

    for job_item in job_logs_description:
        group, job_id, git_root_nickname = job_item["logStreamName"].split("/")
        if job_id not in jobs_details_from_batch:
            continue
        jobs_listed.append(job_id)

        vulns_summary: Optional[RootMachineExecutionItem] = None

        if git_root_nickname in group_roots.values():
            job_items.append(
                Job(
                    created_at=jobs_details_from_batch[job_id].get(
                        "createdAt"
                    ),
                    exit_code=jobs_details_from_batch[job_id]
                    .get("container", {})
                    .get("exitCode"),
                    exit_reason=jobs_details_from_batch[job_id]
                    .get("container", {})
                    .get("reason"),
                    id=jobs_details_from_batch[job_id]["jobId"],
                    name=f"skims-process-{group}-{git_root_nickname}",
                    root_nickname=job_item["logStreamName"].split("/")[-1],
                    queue=jobs_details_from_batch[job_id]["jobQueue"].split(
                        "/"
                    )[-1],
                    started_at=job_item.get("firstEventTimestamp", 0),
                    stopped_at=job_item.get("lastEventTimestamp", 0),
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
        response = await list_jobs(
            queue=queue,
            filters=[{"name": "JOB_NAME", "values": [filters]}],
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


async def queue_job_new(
    group_name: str,
    finding_codes: Union[Tuple[str, ...], List[str]],
    queue: SkimsBatchQueue = SkimsBatchQueue.HIGH,
    roots: Optional[Union[Tuple[str, ...], List[str]]] = None,
    dataloaders: Any = None,
    **kwargs: Any,
) -> Optional[str]:
    if not roots:
        if not dataloaders:
            raise Exception(
                (
                    "If you don't provide the roots parameter, you must"
                    " provide the dataloaders parameter to load the roots"
                )
            )
        roots = list(
            root.state.nickname
            for root in await dataloaders.group_roots.load(group_name)
            if isinstance(root, GitRootItem)
            and root.state.status == "ACTIVE"
            and root.cloning.status == GitCloningStatus.OK
        )

    if not roots:
        return None

    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )

    current_executions = await get_actions_by_name(
        action_name="execute-machine", entity=group_name
    )
    current_executions = tuple(
        sorted(current_executions, key=lambda x: int(x.time))
    )
    for execution in current_executions:
        exc_info = json.loads(execution.additional_info)
        roots = tuple({*roots, *exc_info["roots"]})
        finding_codes = tuple({*finding_codes, *exc_info["checks"]})

    dynamodb_pk = current_executions[-1].key if current_executions else None

    async with aioboto3.Session().client(**resource_options) as batch:
        for execution in current_executions[:-1]:
            await delete_action(dynamodb_pk=execution.key)
            if job_id := execution.batch_job_id:
                await batch.terminate_job(jobId=job_id, reason="not required")
                await batch.cancel_job(jobId=job_id, reason="not required")

    return (
        await put_action(
            action_name="execute-machine",
            vcpus=4,
            product_name="skims",
            queue=queue.value,
            entity=group_name,
            additional_info=json.dumps(
                {
                    "roots": list(roots),
                    "checks": list(finding_codes),
                }
            ),
            attempt_duration_seconds=86400,
            subject="integrates@fluidattacks.com",
            dynamodb_pk=dynamodb_pk,
            **kwargs,
        )
    ).success


def _get_seconds_ago(timestamp: int) -> float:
    date = datetime.datetime.fromtimestamp(int(timestamp / 1000))
    now = datetime.datetime.utcnow()
    return (now - date).seconds


async def get_active_executions(root: GitRootItem) -> LastMachineExecutions:
    group: str = root.group_name
    complete_jobs_response = await collect(
        list_jobs(
            queue=queue.value,
            filters=[
                {"name": "JOB_NAME", "values": [f"skims-process-{group}"]}
            ],
            maxResults=1,
        )
        for queue in SkimsBatchQueue
    )
    specific_jobs_response = await list_jobs(
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
        and (
            root.state.nickname
            in specific_job_description[0]["container"]["command"][-1]
            or any(
                env["name"] == "MAKES_AWS_BATCH_COMPAT"
                for env in specific_job_description[0]["container"][
                    "environment"
                ]
            )
        )
        else None,
    )
