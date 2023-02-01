import aioboto3
from aioextensions import (
    collect,
)
from context import (
    FI_AWS_REGION_NAME,
)
from custom_exceptions import (
    RootNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.roots.get import (
    get_machine_executions_by_job_id,
)
from db_model.roots.types import (
    GitRoot,
    RootMachineExecution,
    RootRequest,
)
from more_itertools import (
    collapse,
)
from s3.resource import (
    get_s3_resource,
)
from schedulers.common import (
    info,
)
from typing import (
    Any,
    cast,
    Optional,
)


async def process_item(
    *,
    loaders: Dataloaders,
    s3_client: Any,
    job: RootMachineExecution,
) -> bool:
    group_name = job.name.split("-")[-1]
    try:
        git_root = cast(
            GitRoot,
            await loaders.root.load(RootRequest(group_name, job.root_id)),
        )
    except RootNotFound:
        return False
    result_objects = (
        await s3_client.list_objects(
            Bucket="machine.data",
            Prefix=(
                f"results/{group_name}_{job.job_id}"
                f"_{git_root.state.nickname}"
            ),
        )
    ).get("Contents", [])
    config_objects = (
        await s3_client.list_objects(
            Bucket="machine.data",
            Prefix=(
                f"configs/{group_name}_{job.job_id}"
                f"_{git_root.state.nickname}"
            ),
        )
    ).get("Contents", [])
    if not result_objects or not config_objects:
        return False
    return True


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    current_date = datetime.now()

    session = aioboto3.Session(region_name=FI_AWS_REGION_NAME)
    batch_jobs: tuple[dict[str, Any], ...] = tuple()
    async with session.client("batch") as client:
        next_token: Optional[str] = ""
        while next_token is not None:
            response = await client.list_jobs(
                jobQueue="medium",
                maxResults=100,
                filters=[
                    {
                        "name": "AFTER_CREATED_AT",
                        "values": [
                            str(
                                int(
                                    (
                                        current_date - timedelta(days=1)
                                    ).timestamp()
                                    * 1000
                                )
                            ),
                        ],
                    },
                ],
                nextToken=next_token,
            )
            batch_jobs = (
                *batch_jobs,
                *(
                    job
                    for job in response["jobSummaryList"]
                    if job["jobName"].startswith("skims-execute-machine")
                    and job["status"] == "SUCCEEDED"
                ),
            )
            next_token = response.get("nextToken")

    jobs_in_db: tuple[RootMachineExecution, ...] = tuple(
        collapse(
            await collect(
                [
                    get_machine_executions_by_job_id(job_id=job["jobId"])
                    for job in batch_jobs
                ],
                workers=100,
            ),
            base_type=RootMachineExecution,
        )
    )
    jobs_in_db = tuple(
        job
        for job in jobs_in_db
        if job.started_at is None or job.stopped_at is None
    )
    info("%s jobs cloud be modified", len(jobs_in_db))
    s3_client = await get_s3_resource()
    futures = [
        process_item(
            loaders=loaders,
            s3_client=s3_client,
            job=job,
        )
        for job in jobs_in_db
    ]
    result = await collect(futures, workers=100)
    info("%s jobs are modified", result.count((True)))
