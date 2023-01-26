from aioextensions import (
    collect,
)
from batch.dal import (
    describe_jobs,
    get_actions_by_name,
    put_action,
    SkimsBatchQueue,
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
from custom_exceptions import (
    RootAlreadyCloning,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.get import (
    get_machine_executions,
)
from db_model.roots.types import (
    GitRoot,
    RootMachineExecution,
)
import json
import logging
import logging.config
from more_itertools import (
    collapse,
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


class JobArguments(NamedTuple):
    group_name: str
    finding_code: str
    root_nickname: str


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


def _get_job_execution_time(
    job_execution_time: Optional[datetime],
    action_time: str,
    batch_jobs_dict: Dict[str, Any],
    job_execution: RootMachineExecution,
) -> Optional[int]:
    if job_execution_time:
        return int(job_execution_time.timestamp() * 1000)
    if job_execution.status:
        return batch_jobs_dict.get(
            job_execution.job_id, {action_time: None}
        ).get(action_time)
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
                created_at=int(job_execution.created_at.timestamp() * 1000),
                exit_code=0,
                exit_reason="",
                id=job_execution.job_id,
                name=job_execution.name,
                root_nickname=group_roots[job_execution.root_id],
                queue=job_execution.queue,
                started_at=_get_job_execution_time(
                    job_execution.started_at,
                    "startedAt",
                    batch_jobs_dict,
                    job_execution,
                ),
                stopped_at=_get_job_execution_time(
                    job_execution.stopped_at,
                    "stoppedAt",
                    batch_jobs_dict,
                    job_execution,
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
    loaders: Dataloaders,
    user_email: str,
    group_name: str,
    roots: Optional[Tuple[GitRoot, ...]] = None,
    check_existing_jobs: bool = True,
    force: bool = False,
    queue_with_vpn: bool = False,
) -> Optional[PutActionResult]:

    from roots import (  # pylint: disable=import-outside-toplevel
        domain as roots_domain,
    )

    try:
        return await roots_domain.queue_sync_git_roots(
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


async def queue_job_new(  # pylint: disable=too-many-arguments
    group_name: str,
    dataloaders: Dataloaders,
    finding_codes: Union[Tuple[str, ...], List[str]],
    queue: SkimsBatchQueue = SkimsBatchQueue.SMALL,
    roots: Optional[Union[Tuple[str, ...], List[str]]] = None,
    clone_before: bool = False,
    **kwargs: Any,
) -> Optional[PutActionResult]:
    queue_result: Optional[PutActionResult] = None
    group: Group = await dataloaders.group.load(group_name)
    if (
        group.state.has_machine
        and group.state.managed != GroupManaged.UNDER_REVIEW
    ):
        group_roots = await dataloaders.group_roots.load(group_name)
        group_git_roots: List[GitRoot] = [
            root
            for root in group_roots
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
        ]
        if not roots:
            roots = list(
                root.state.nickname
                for root in group_git_roots
                if (
                    (root.state.credential_id is not None and clone_before)
                    or not clone_before
                )
            )

        if roots:
            if (
                clone_before
                and (
                    result_clone := (
                        await _queue_sync_git_roots(
                            loaders=dataloaders,
                            user_email="integrates@fluidattacks.com",
                            group_name=group_name,
                            force=True,
                            roots=tuple(
                                root
                                for root in group_git_roots
                                if root.state.nickname in roots
                            ),
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
                vcpus=2,
                product_name=Product.SKIMS,
                queue=queue,
                entity=group_name,
                additional_info=json.dumps(
                    {
                        "roots": list(sorted(roots)),
                        "checks": list(sorted(finding_codes)),
                    }
                ),
                attempt_duration_seconds=43200,
                subject="integrates@fluidattacks.com",
                memory=3700,
                **kwargs,
            )

            await collect(
                [
                    add_machine_execution(
                        root_id=root.id,
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
                    for root in group_git_roots
                    if (
                        root.state.nickname in roots
                        and queue_result.batch_job_id
                    )
                ]
            )

    return queue_result


__all__ = [
    "SkimsBatchQueue",
]
