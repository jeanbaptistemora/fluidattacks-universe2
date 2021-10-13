from aioextensions import (
    collect,
)
from back.src.db_model.roots.update import (
    update_git_root_machine_execution,
)
from botocore.exceptions import (
    ClientError,
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
from newutils.utils import (
    get_key_or_fallback,
)
from schedulers.common import (
    info,
    machine_queue,
)
import skims_sdk
from typing import (
    Any,
    Dict,
    List,
    Tuple,
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

            for check in skims_sdk.FINDINGS:
                if skims_sdk.is_check_available(check):
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
