import aioboto3
from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    describe_jobs,
    get_action,
    get_actions_by_name,
    list_jobs_by_status,
    list_log_streams,
    put_action,
)
from batch.enums import (
    Action,
    JobStatus,
    Product,
)
from batch.types import (
    Job,
    PutActionResult,
    VulnerabilitiesSummary,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
)
from dateutil.parser import (  # type: ignore
    parse as date_parse,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.get import (
    get_machine_executions,
)
from db_model.roots.types import (
    GitRootItem,
    LastMachineExecutions,
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
from roots.types import (
    GitRoot,
)
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
LOGGER = logging.getLogger("console")
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
        if item["jobName"].startswith == f"skims-execute-machine-{group_name}"
    }
    jobs_details_from_batch = {}
    for item in await describe_jobs(*jobs_runnable_from_batch.keys()):
        if action := await get_action(
            action_dynamo_pk=item["container"]["command"][4]
        ):
            if finding_code in json.loads(action.additional_info)["checks"]:
                jobs_details_from_batch[item["jobId"]] = item
        else:
            jobs_details_from_batch[item["jobId"]] = item

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

    for job_execution in jobs_from_db:
        _vulns = [
            x
            for x in job_execution.findings_executed
            if x.finding == finding_code
        ]
        job_items.append(
            Job(
                created_at=int(
                    date_parse(job_execution.created_at).timestamp() * 1000
                ),
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
                )
                if job_execution.stopped_at is not None
                else None,
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
        group, job_id, git_root_nickname = str(
            job_item["logStreamName"]
        ).split("/")
        if job_id not in jobs_details_from_batch:
            continue

        vulns_summary: Optional[VulnerabilitiesSummary] = None

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
                    root_nickname=str(job_item["logStreamName"]).rsplit(
                        "/", maxsplit=1
                    )[-1],
                    queue=jobs_details_from_batch[job_id]["jobQueue"].split(
                        "/"
                    )[-1],
                    started_at=int(job_item.get("firstEventTimestamp", 0)),
                    stopped_at=int(job_item.get("lastEventTimestamp", 0)),
                    status=jobs_details_from_batch[job_id]["status"],
                    vulnerabilities=vulns_summary,
                )
            )
    return sorted(
        job_items,
        key=lambda job: job.created_at or 0,
        reverse=True,
    )


async def queue_job_new(
    group_name: str,
    finding_codes: Union[Tuple[str, ...], List[str]],
    queue: SkimsBatchQueue = SkimsBatchQueue.HIGH,
    roots: Optional[Union[Tuple[str, ...], List[str]]] = None,
    dataloaders: Any = None,
    **kwargs: Any,
) -> Optional[PutActionResult]:
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

    current_executions = tuple(
        execution
        for execution in await get_actions_by_name(
            action_name="execute-machine", entity=group_name
        )
        if execution.queue == queue.value
    )
    current_executions = tuple(
        sorted(current_executions, key=lambda x: int(x.time))
    )
    for execution in current_executions:
        exc_info = json.loads(execution.additional_info)
        roots = tuple({*roots, *exc_info["roots"]})
        finding_codes = tuple({*finding_codes, *exc_info["checks"]})

    dynamodb_pk = (
        current_executions[-1].key
        if current_executions and not current_executions[-1].running
        else None
    )

    async with aioboto3.Session().client(**resource_options) as batch:
        for execution in current_executions[:-1]:
            if not execution.running:
                LOGGER.info(
                    "There is already a job in queue, %s will be removed",
                    execution.key,
                    extra={"extra": None},
                )
                await delete_action(dynamodb_pk=execution.key)
                if job_id := execution.batch_job_id:
                    await batch.terminate_job(
                        jobId=job_id, reason="not required"
                    )
                    await batch.cancel_job(jobId=job_id, reason="not required")

    return await put_action(
        action=Action.EXECUTE_MACHINE,
        vcpus=4,
        product_name=Product.SKIMS,
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


async def get_active_executions(root: GitRoot) -> LastMachineExecutions:
    group: str = root.group_name
    queued_jobs_dict = {
        job.batch_job_id: job
        for job in await get_actions_by_name(
            action_name="execute-machine", entity=group
        )
        if job.batch_job_id and json.loads(job.additional_info)["roots"]
    }
    jobs_from_batch = await describe_jobs(*queued_jobs_dict.keys())

    active_jobs_from_batch = tuple(
        RootMachineExecutionItem(
            job_id=entry_execution["jobId"],
            created_at=datetime_utils.get_as_str(
                datetime_utils.get_datetime_from_batch(
                    entry_execution["createdAt"]
                )
            ),
            started_at=datetime_utils.get_as_str(
                datetime_utils.get_datetime_from_batch(
                    entry_execution["startedAt"]
                )
            )
            if "startedAt" in entry_execution
            else None,
            stopped_at=datetime_utils.get_as_str(
                datetime_utils.get_datetime_from_batch(
                    entry_execution["stoppedAt"]
                )
            )
            if "stoppedAt" in entry_execution
            else None,
            name=f"skims-process-{group}-{root_nickname}",
            queue=queued_jobs_dict[entry_execution["jobId"]].queue,
            root_id=root.id,
            findings_executed=[],
        )
        for entry_execution in jobs_from_batch
        for root_nickname in json.loads(
            queued_jobs_dict[entry_execution["jobId"]].additional_info
        )["roots"]
        if root_nickname == root.nickname
    )

    active_urgent_jobs = tuple(
        job
        for job in active_jobs_from_batch
        if job.queue == SkimsBatchQueue.HIGH.value
    )
    active_normal_jobs = tuple(
        job
        for job in active_jobs_from_batch
        if job.queue == SkimsBatchQueue.LOW.value
    )

    return LastMachineExecutions(
        complete=active_normal_jobs[0] if active_normal_jobs else None,
        specific=active_urgent_jobs[0] if active_urgent_jobs else None,
    )
