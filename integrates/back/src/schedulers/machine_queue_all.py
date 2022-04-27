import aioboto3
from aioextensions import (
    collect,
)
from batch.types import (
    PutActionResult,
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
from db_model.groups.types import (
    Group,
)
from machine.availability import (
    is_check_available,
)
from machine.jobs import (
    FINDINGS,
    queue_job_new,
    SkimsBatchQueue,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    error,
    info,
)
from typing import (
    Any,
    NamedTuple,
    Optional,
)


class RootsByGroup(NamedTuple):
    roots: list[str]
    group_name: str


class PreparedJob(NamedTuple):
    group_name: str
    roots: list[str]
    last_queue: Optional[float] = 0


async def _queue_all_checks(
    loaders: Dataloaders,
    group_name: str,
    finding_codes: tuple[str, ...],
) -> Optional[PutActionResult]:
    result = await queue_job_new(
        dataloaders=loaders,
        group_name=group_name,
        finding_codes=finding_codes,
        queue=SkimsBatchQueue.LOW,
    )
    if result:
        info(
            "Queued %s with the follow identifier %s",
            group_name,
            result.dynamo_pk,
        )
    else:
        error("A queuing error has occurred %s", group_name)
    return result


def _is_check_available(check: str) -> bool:
    with suppress(NotImplementedError):
        return is_check_available(check)
    return False


async def get_jobs_from_bach(*job_ids: str) -> list[dict[str, Any]]:
    jobs = list(job_ids)
    if not jobs:
        return []
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.Session().client(**resource_options) as batch:
        try:
            result = await batch.describe_jobs(jobs=jobs)
            return result["jobs"]
        except ClientError:
            return []


async def _roots_by_group(
    loaders: Dataloaders,
    group: Group,
) -> RootsByGroup:
    if group.state.has_machine:
        return RootsByGroup(
            group_name=group.name,
            roots=[],
        )
    return RootsByGroup(
        group_name=group.name,
        roots=[
            root.state.nickname
            for root in await loaders.group_roots.load(group.name)
            if root.state.status == "ACTIVE"
        ],
    )


async def main() -> None:
    session = aioboto3.Session()
    loaders: Dataloaders = get_new_context()
    async with session.client("s3") as s3_client:
        all_active_groups = await orgs_domain.get_all_active_groups_typed(
            loaders
        )
        group_names: list[str] = [
            prefix["Prefix"].split("/")[0]
            for response in await collect(
                s3_client.list_objects(
                    Bucket="continuous-repositories",
                    Prefix=group.name,
                    Delimiter="/",
                    MaxKeys=1,
                )
                for group in all_active_groups
            )
            for prefix in response.get("CommonPrefixes", [])
        ]
    findings = [key for key in FINDINGS.keys() if _is_check_available(key)]
    _groups_roots: list[RootsByGroup] = await collect(
        [
            _roots_by_group(loaders, group)
            for group in await loaders.group_typed.load_many(group_names)
        ]
    )

    jobs: dict[str, PreparedJob] = {
        root.group_name: PreparedJob(
            group_name=root.group_name, roots=root.roots
        )
        for root in _groups_roots
        if root
    }
    info("Computing jobs")

    sorted_jobs: list[PreparedJob] = list(
        sorted(
            jobs.values(),
            key=lambda x: x.last_queue or 0,
        )
    )
    all_job_futures = [
        _queue_all_checks(
            loaders=loaders,
            group_name=prepared_job.group_name,
            finding_codes=tuple(findings),
        )
        for prepared_job in sorted_jobs
        if len(prepared_job.roots) > 0
    ]
    await collect(all_job_futures)
