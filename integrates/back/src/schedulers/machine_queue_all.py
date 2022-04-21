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
    queue_job_new,
    SkimsBatchQueue,
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
    group: str,
    finding_codes: tuple[str, ...],
    dataloaders: Any,
) -> dict[str, Any]:
    result = await queue_job_new(
        group_name=group,
        finding_codes=finding_codes,
        queue=SkimsBatchQueue.LOW,
        dataloaders=dataloaders,
    )
    if result:
        info(
            "Queued %s with the follow identifier %s", group, result.dynamo_pk
        )
    else:
        error("A queuing error has occurred %s", group)
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
    group: str, group_conf: dict[Any, Any], dataloaders: Dataloaders
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
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        groups: list[str] = [
            prefix["Prefix"].split("/")[0]
            for response in await collect(
                s3_client.list_objects(
                    Bucket="continuous-repositories",
                    Prefix=group,
                    Delimiter="/",
                    MaxKeys=1,
                )
                for group in await get_active_groups()
            )
            for prefix in response.get("CommonPrefixes", [])
        ]
    dataloaders: Dataloaders = get_new_context()
    groups_data = await collect(
        get_attributes(group, ["historic_configuration"]) for group in groups
    )
    groups_confs = [
        group_data["historic_configuration"][-1] for group_data in groups_data
    ]
    findings = [key for key in FINDINGS.keys() if _is_check_available(key)]
    _groups_roots: list[RootsByGroup] = await collect(
        [
            _roots_by_group(group, conf, dataloaders)
            for group, conf in zip(groups, groups_confs)
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
            group=prepared_job.group_name,
            finding_codes=tuple(findings),
            dataloaders=dataloaders,
        )
        for prepared_job in sorted_jobs
        if len(prepared_job.roots) > 0
    ]
    await collect(all_job_futures)
