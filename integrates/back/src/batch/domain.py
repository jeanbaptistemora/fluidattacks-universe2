from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    JobStatus,
)
from batch.types import (
    BatchProcessing,
    JobPayload,
)
from typing import (
    List,
    Set,
)


def format_job_payload(job_description: BatchProcessing) -> JobPayload:
    return JobPayload(
        action_name=job_description.action_name,
        subject=job_description.subject,
        entity=job_description.entity,
        time=job_description.time,
        additional_info=job_description.additional_info,
    )


async def get_job_payloads(
    queues: List[str], statuses: List[JobStatus]
) -> Set[JobPayload]:
    queues_jobs = await batch_dal.list_queues_jobs(
        queues=queues, statuses=statuses
    )
    loaded_jobs = await batch_dal.decribe_jobs(
        set(queues_jobs.id for queues_jobs in queues_jobs)
    )
    action_dynamo_pk_position: int = 4
    filtered_loaded_jobs = [
        job_description
        for job_description in loaded_jobs
        if len(job_description.container.command) > action_dynamo_pk_position
    ]
    dynamo_jobs = await collect(
        tuple(
            batch_dal.get_action(
                action_dynamo_pk=job_description.container.command[
                    action_dynamo_pk_position
                ]
            )
            for job_description in filtered_loaded_jobs
        ),
        workers=32,
    )
    return {
        format_job_payload(dynamo_job)
        for _, dynamo_job in zip(filtered_loaded_jobs, dynamo_jobs)
        if dynamo_job
    }
