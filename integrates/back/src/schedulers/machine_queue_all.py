import aioboto3
from aioextensions import (
    collect,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
)
from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from groups.domain import (
    get_active_groups,
    get_attributes,
)
from machine.availability import (
    is_check_available,
)
from machine.jobs import (
    FINDINGS,
    list_jobs_filter,
    queue_all_checks_new,
)
from newutils.utils import (
    get_key_or_fallback,
)
from schedulers.common import (
    error,
    info,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
)


class RootsByGroup(NamedTuple):
    roots: List[str]
    group_name: str


class PreparedJob(NamedTuple):
    group_name: str
    roots: List[str]
    last_queue: Optional[float] = 0


async def _queue_all_checks(
    group: str,
    repos: List[str],
    finding_codes: List[str],
) -> Dict[str, Any]:
    result = await queue_all_checks_new(group, repos, finding_codes)
    if result:
        info("Queued %s", group)
    else:
        error("A queuing error has occurred %s", group)
    return result


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
            result = await batch.describe_jobs(jobs=jobs)
            return result["jobs"]
        except ClientError:
            return []


async def get_job_groups_from_bach(*groups: str) -> List[Dict[str, Any]]:
    if not groups:
        return []

    jobs = []
    next_token: Optional[str] = None
    while True:
        result = await list_jobs_filter(
            "skims_all_later",
            filters=[
                {
                    "name": "JOB_NAME",
                    "values": [f"skims-process-{group}" for group in groups],
                }
            ],
        )
        next_token = result.get("nextToken")
        jobs.extend(
            [
                {"group": data.split("-")[-1], **data}
                for data in result.get("jobSummaryList", [])
            ]
        )

        if not next_token:
            break

    return jobs


async def _roots_by_group(
    group: str, group_conf: Dict[Any, Any], dataloaders: Dataloaders
) -> RootsByGroup:
    if not get_key_or_fallback(group_conf, "has_machine", "has_skims", False):
        return RootsByGroup(
            group_name=group,
            roots=[],
        )
    return RootsByGroup(
        group_name=group,
        roots=[
            root.state.nickname
            for root in await dataloaders.group_roots.load(group)
            if root.state.status == "ACTIVE"
        ],
    )


async def main() -> None:
    groups: List[str] = await get_active_groups()
    dataloaders: Dataloaders = get_new_context()
    groups_data = await collect(
        get_attributes(group, ["historic_configuration"]) for group in groups
    )
    groups_confs = [
        group_data["historic_configuration"][-1] for group_data in groups_data
    ]
    findings = [key for key in FINDINGS.keys() if _is_check_available(key)]
    _groups_roots: List[RootsByGroup] = await collect(
        [
            _roots_by_group(group, conf, dataloaders)
            for group, conf in zip(groups, groups_confs)
        ]
    )

    jobs: Dict[str, PreparedJob] = {
        root.group_name: PreparedJob(
            group_name=root.group_name, roots=root.roots
        )
        for root in _groups_roots
        if root
    }
    info("Computing jobs")

    jobs_batch = await get_job_groups_from_bach(*(job[0] for job in jobs))

    for job_batch in jobs_batch:
        group = job_batch["group"]
        if jobs[group].last_queue != 0:
            continue
        jobs[group] = PreparedJob(
            group_name=jobs[group].group_name,
            roots=jobs[group].roots,
            last_queue=job_batch.get("createdAt", 0),
        )

    sorted_jobs: List[PreparedJob] = list(
        sorted(
            jobs.values(),
            key=lambda x: x.last_queue or 0,
        )
    )
    all_job_futures = [
        _queue_all_checks(
            group=prepared_job.group_name,
            repos=prepared_job.roots,
            finding_codes=findings,
        )
        for prepared_job in sorted_jobs
        if len(prepared_job.roots) > 0
    ]
    await collect(all_job_futures)
