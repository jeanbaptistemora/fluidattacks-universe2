import aioboto3
from aioextensions import (
    collect,
)
from back.src.context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
)
from back.src.db_model.roots.update import (
    update_git_root_machine_execution,
)
from back.src.machine.availability import (
    is_check_available,
)
from back.src.machine.jobs import (
    FINDINGS,
)
from botocore.exceptions import (
    ClientError,
)
from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import datetime
import dateutil.parser  # type: ignore
from groups.domain import (
    get_active_groups,
    get_attributes,
    LOGGER_CONSOLE,
)
from more_itertools import (
    chunked,
    collapse,
)
from newutils.utils import (
    get_key_or_fallback,
)
from schedulers.common import (
    info,
    machine_queue,
)
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
)


class PreparedJob(NamedTuple):
    root_id: str
    group_name: str
    check: str
    root_nick_name: str
    execution_date: Optional[float]
    batch_job_id: Optional[str]


def _is_check_available(check: str) -> bool:
    with suppress(NotImplementedError):
        return is_check_available(check)
    return False


async def get_jobs_from_bach(*job_ids: str) -> List[Dict[str, Any]]:
    jobs = list(job_ids)
    if not jobs:
        return []
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.client(**resource_options) as batch:
        try:
            result = await batch.describe_jobs(jobs=list(job_ids))
            return result["jobs"]
        except ClientError:
            return []


async def filer_already_in_queue(
    jobs: Iterable[PreparedJob],
) -> Tuple[PreparedJob, ...]:
    futures = (
        get_jobs_from_bach(
            *[job.batch_job_id for job in set_jobs if job.batch_job_id]
        )
        for set_jobs in chunked(jobs, 100)
    )
    jobs_status = {
        _job["jobId"]: _job["status"]
        for _job in collapse(await collect(futures), base_type=dict)
    }

    return tuple(
        _job
        for _job in jobs
        if _job.batch_job_id is None
        or (
            _job.batch_job_id
            and jobs_status.get(_job.batch_job_id, "NEVER_EXECUTED")
            in ("SUCCEEDED", "FAILED", "NEVER_EXECUTED")
        )
    )


async def _jobs_by_group(
    group: str, group_conf: Dict[Any, Any], dataloaders: Dataloaders
) -> List[Tuple[str, str, str, str, float]]:
    result: List[Tuple[str, str, str, str, float]] = []
    if not get_key_or_fallback(group_conf, "has_machine", "has_skims", False):
        return result
    for root in await dataloaders.group_roots.load(group):
        if root.state.status == "ACTIVE":
            try:
                executions = root.machine_execution
            except AttributeError:
                continue
            map_executions = {
                execution.finding_code: dateutil.parser.parse(
                    execution.queue_date
                ).timestamp()
                for execution in executions
            }

            for check in FINDINGS:
                if _is_check_available(check):
                    result.append(
                        (
                            root.id,
                            group,
                            check,
                            root.state.nickname,
                            map_executions.get(check, 0),
                        )
                    )
    return result


async def _machine_queue(
    root_id: str,
    finding_code: str,
    group_name: str,
    namespace: str,
    urgent: bool,
) -> Tuple[Dict[str, Any], str, str, str, str]:
    try:
        result = await machine_queue(
            finding_code=finding_code,
            group_name=group_name,
            namespace=namespace,
            urgent=urgent,
        )
    except ClientError as exc:
        LOGGER_CONSOLE.exception(exc, exc_info=True)
        return ({}, root_id, group_name, finding_code, namespace)

    if result and (job_id := result.get("jobId")):
        await update_git_root_machine_execution(
            group_name,
            root_id,
            finding_code,
            datetime.datetime.now().isoformat(),
            job_id,
        )
        info(
            "queued %s-%s-%s",
            group_name,
            finding_code,
            namespace,
            extra={"root_id": root_id, "batch_id": job_id},
        )
    else:
        info(
            "the job has not been queued %s-%s-%s",
            group_name,
            finding_code,
            namespace,
            extra={"root_id": root_id},
        )
    return (result, root_id, group_name, finding_code, namespace)


async def main() -> None:
    groups: List[str] = await get_active_groups()
    dataloaders: Dataloaders = get_new_context()
    groups_data = await collect(
        get_attributes(group, ["historic_configuration"]) for group in groups
    )
    groups_confs = [
        group_data["historic_configuration"][-1] for group_data in groups_data
    ]

    info("Computing jobs")
    # compute all jobs in parallel
    group_jobs = await collect(
        _jobs_by_group(group, group_conf, dataloaders)
        for group, group_conf in zip(groups, groups_confs)
    )
    all_jobs = []
    for _jobs in group_jobs:
        all_jobs.extend(_jobs)
    info("jobs to queue %s", len(all_jobs))
    jobs_by_finding: Dict[str, List[Tuple[float, str, str, str, str]]] = {}
    for _job in all_jobs:
        check = _job[2]
        if check not in jobs_by_finding.keys():
            jobs_by_finding[check] = [_job]
        else:
            jobs_by_finding[check].append(_job)

    for finding, _jobs in jobs_by_finding.items():
        info("%s will be queued for finding %s", len(_jobs), finding)
        sorted_jobs = list(sorted(_jobs, key=lambda x: x[4]))
        all_jobs_futers = [
            _machine_queue(
                root_id=root_id,
                finding_code=finding,
                group_name=group,
                namespace=namespace,
                urgent=False,
            )
            for root_id, group, finding, namespace, _ in sorted_jobs
        ]
        await collect(all_jobs_futers)
