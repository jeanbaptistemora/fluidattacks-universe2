import aioboto3
from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
    describe_jobs,
    get_actions_by_name,
    put_action,
)
from batch.enums import (
    Action,
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
from custom_exceptions import (
    RootAlreadyCloning,
)
from datetime import (
    datetime,
)
from dateutil.parser import (  # type: ignore
    parse as date_parse,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.get import (
    get_machine_executions,
)
from db_model.roots.types import (
    GitRoot,
    LastMachineExecutions,
    MachineFindingResult,
    RootMachineExecution,
)
from enum import (
    Enum,
)
import json
import logging
import logging.config
from more_itertools import (
    collapse,
)
from newutils import (
    datetime as datetime_utils,
)
import os
from roots.domain import (
    add_machine_execution,
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
LOGGER = logging.getLogger(__name__)
QUEUES: Dict[str, Dict[str, str]] = _json_load(os.environ["MACHINE_QUEUES"])
FINDINGS: Dict[str, Dict[str, Dict[str, str]]] = _json_load(
    os.environ["MACHINE_FINDINGS"]
)


class SkimsBatchQueue(Enum):
    SMALL: str = "small"
    MEDIUM: str = "medium"
    LARGE: str = "large"
    CLONE: str = "clone"


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
    group_roots: Dict[str, str],
) -> List[Job]:
    jobs_from_db: Tuple[RootMachineExecution, ...] = tuple(
        execution
        for execution in collapse(
            (
                await collect(
                    get_machine_executions(root_id=root_id)
                    for root_id in group_roots.keys()
                )
            ),
            base_type=RootMachineExecution,
        )
        if any(
            find.finding == finding_code
            for find in execution.findings_executed
        )
    )
    batch_jobs_dict = {
        item["jobId"]: item
        for item in await describe_jobs(
            *{item.job_id for item in jobs_from_db}
        )
    }
    job_items = []

    for job_execution in jobs_from_db:
        if job_execution.job_id not in batch_jobs_dict or (
            # prevent terminated job
            job_execution.status in {"RUNNING", "RUNNABLE"}
            and batch_jobs_dict[job_execution.job_id]["status"] == "FAILED"
        ):
            continue
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
                )
                if job_execution.started_at is not None
                else (
                    batch_jobs_dict.get(
                        job_execution.job_id, {"startedAt": None}
                    ).get("startedAt")
                    if job_execution.status is None
                    else None
                ),
                stopped_at=int(
                    date_parse(job_execution.stopped_at).timestamp() * 1000
                )
                if job_execution.stopped_at is not None
                else (
                    batch_jobs_dict.get(
                        job_execution.job_id, {"stoppedAt": None}
                    ).get("stoppedAt")
                    if job_execution.status is None
                    else None
                ),
                status=job_execution.status
                or ("SUCCESS" if job_execution.success else "FAILED"),
                vulnerabilities=VulnerabilitiesSummary(
                    modified=_vulns[0].modified, open=_vulns[0].open
                ),
            )
        )

    return sorted(
        job_items,
        key=lambda job: job.created_at or 0,
        reverse=True,
    )


async def _queue_sync_git_roots(
    *,
    loaders: Any,
    user_email: str,
    group_name: str,
    roots: Optional[Tuple[GitRoot, ...]] = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
) -> Optional[PutActionResult]:
    from batch.actions import (  # pylint: disable=import-outside-toplevel
        clone_roots,
    )

    try:
        return await clone_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=user_email,
            group_name=group_name,
            roots=roots,
            check_existing_jobs=check_existing_jobs,
            force=force,
            queue_with_vpn=queue_with_vpn,
        )
    except RootAlreadyCloning:
        current_jobs = sorted(
            await get_actions_by_name("clone_roots", group_name),
            key=lambda x: x.time,
        )
        if current_jobs:
            return PutActionResult(
                success=True,
                batch_job_id=current_jobs[0].batch_job_id,
                dynamo_pk=current_jobs[0].key,
            )
    return None


async def queue_job_new(  # pylint: disable=too-many-arguments,too-many-locals
    group_name: str,
    dataloaders: Any,
    finding_codes: Union[Tuple[str, ...], List[str]],
    queue: SkimsBatchQueue = SkimsBatchQueue.MEDIUM,
    roots: Optional[Union[Tuple[str, ...], List[str]]] = None,
    clone_before: bool = False,
    **kwargs: Any,
) -> Optional[PutActionResult]:
    git_roots: List[GitRoot] = []
    if dataloaders:
        git_roots = await dataloaders.group_roots.load(group_name)

    if not roots:
        roots = list(
            root.state.nickname
            for root in git_roots
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
            and root.cloning.status == GitCloningStatus.OK
        )

    if not roots:
        return None

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

    async with aioboto3.Session().client(
        **(
            dict(
                service_name="batch",
                aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
                aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
            )
        )
    ) as batch:
        for execution in current_executions[:-1]:
            if not execution.running:
                LOGGER.info(
                    "There is already a job in queue, %s will be removed",
                    execution.key,
                )
                await delete_action(dynamodb_pk=execution.key)
                if job_id := execution.batch_job_id:
                    await batch.terminate_job(
                        jobId=job_id, reason="not required"
                    )
                    await batch.cancel_job(jobId=job_id, reason="not required")

    if (
        (clone_before and dataloaders)
        and (
            result_clone := (
                await _queue_sync_git_roots(
                    loaders=dataloaders,
                    user_email="integrates@fluidattacks.com",
                    group_name=group_name,
                    force=True,
                )
            )
        )
        and (clone_job_id := result_clone.batch_job_id)
    ):
        kwargs["dependsOn"] = [
            {"jobId": clone_job_id, "type": "SEQUENTIAL"},
        ]
    queue_result = await put_action(
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
        memory=7200,
        **kwargs,
    )

    if git_roots:
        await collect(
            [
                add_machine_execution(
                    root_id=git_root_item.id,
                    job_id=queue_result.batch_job_id,
                    createdAt=datetime.now(),
                    findings_executed=list(
                        {
                            "finding": finding,
                            "open": 0,
                            "modified": 0,
                        }
                        for finding in finding_codes
                    ),
                )
                for git_root_item in git_roots
                if git_root_item.state.nickname in roots
                and queue_result.batch_job_id
            ]
        )

    return queue_result


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
        RootMachineExecution(
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
            findings_executed=[
                MachineFindingResult(open=0, modified=0, finding=fin)
                for fin in json.loads(
                    queued_jobs_dict[entry_execution["jobId"]].additional_info
                )["checks"]
            ],
        )
        for entry_execution in jobs_from_batch
        for root_nickname in json.loads(
            queued_jobs_dict[entry_execution["jobId"]].additional_info
        )["roots"]
        if root_nickname == root.state.nickname
    )

    jobs = tuple(job for job in active_jobs_from_batch)

    return LastMachineExecutions(
        complete=jobs[0] if jobs else None,
        specific=jobs[0] if jobs else None,
    )
