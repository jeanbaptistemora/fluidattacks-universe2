import aioboto3
from aioextensions import (
    collect,
)
from batch.dal import (
    describe_jobs,
    get_action,
    put_action_to_batch,
    terminate_batch_job,
    update_action_to_dynamodb,
)
from batch.enums import (
    Action,
    Product,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
)
from datetime import (
    datetime,
)
import logging
from machine.jobs import (
    SkimsBatchQueue,
)
from more_itertools import (
    flatten,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger("console")

OPTIONS = dict(
    service_name="batch",
    aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    aws_session_token=FI_AWS_SESSION_TOKEN,
)


async def get_all_jobs(client: Any, queue: str, status: str) -> list[str]:
    jobs_to_inspect = []
    next_token = None
    while True:
        response = await client.list_jobs(
            jobQueue=queue,
            jobStatus=status,
            **({"nextToken": next_token} if next_token else {}),
        )
        next_token = response.get("nextToken")
        jobs = response["jobSummaryList"]
        jobs_to_inspect.extend(jobs)
        if not next_token:
            break
    return jobs_to_inspect


async def get_log_streams(log_stream_name: str) -> list[Any]:
    options = OPTIONS.copy()
    options.update({"service_name": "logs"})

    async with aioboto3.Session().client(**options) as cloudwatch:
        return (
            await cloudwatch.get_log_events(
                logGroupName="/aws/batch/job",
                logStreamName=log_stream_name,
                limit=10,
            )
        )["events"]


async def main() -> None:
    async with aioboto3.Session().client(**OPTIONS) as batch:
        jobs = flatten(
            await collect(
                [
                    get_all_jobs(batch, queue=queue, status="RUNNING")
                    for queue in (
                        SkimsBatchQueue.LOW.value,
                        SkimsBatchQueue.HIGH.value,
                    )
                ]
            )
        )

        jobs_description = await describe_jobs(*[job["jobId"] for job in jobs])
        logs = await collect(
            [
                get_log_streams(
                    log_stream_name=job["container"]["logStreamName"]
                )
                for job in jobs_description
            ]
        )
        # filter jobs that have not sent logs in more than an hour
        update_jobs = [
            job
            for job, log in zip(jobs_description, logs)
            if (
                datetime.utcnow()
                - datetime.fromtimestamp(int(log[-1]["timestamp"] / 1000))
            ).seconds
            > 1800
        ]
        # filter out of scope jobs
        exceptions = ["observes"]
        update_jobs = list(
            filter(
                lambda j: all(e not in j["jobName"] for e in exceptions),
                update_jobs,
            )
        )
        # return None
        actions_dict = {
            action.key: action
            for action in (
                await collect(
                    [
                        get_action(
                            action_dynamo_pk=job["container"]["command"][4]
                        )
                        for job in update_jobs
                    ]
                )
            )
            if action is not None
        }

        # launch new jobs with the same action id
        new_jobs_ids = await collect(
            [
                put_action_to_batch(
                    action_name=Action.EXECUTE_MACHINE.value,
                    vcpus=8,
                    queue=SkimsBatchQueue.HIGH.value,
                    entity=action.entity,
                    attempt_duration_seconds=86400,
                    action_dynamo_pk=action.key,
                    product_name=Product.SKIMS.value,
                    memory=15400,
                )
                for action in actions_dict.values()
            ]
        )
        # update actions, set new bath_job_id and set running to False
        await collect(
            [
                update_action_to_dynamodb(
                    key=action_id, running=False, batch_job_id=new_job_id
                )
                for action_id, new_job_id in zip(
                    actions_dict.keys(), new_jobs_ids
                )
                if new_job_id
            ]
        )
        # terminate batch jobs
        await collect(
            [
                terminate_batch_job(job_id=job["jobId"], reason="job peggated")
                for job in update_jobs
            ]
        )
        LOGGER.info(
            "Number of jobs to finish: %s",
            len(actions_dict),
            extra={"extra": None},
        )
        for action in actions_dict.values():
            LOGGER.info(
                "Canceling job %s for group %s",
                action.batch_job_id,
                action.entity,
                extra={"extra": None},
            )
