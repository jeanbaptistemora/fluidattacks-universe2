from batch import (
    dal as batch_dal,
)
from batch.enums import (
    JobStatus,
)
from batch.types import (
    JobDescription,
    JobPayload,
)
from typing import (
    List,
    Set,
)


def format_job_payload(job_description: JobDescription) -> JobPayload:
    return JobPayload(
        action_name=job_description.container.command[4],
        subject=job_description.container.command[5],
        entity=job_description.container.command[6],
        time=job_description.container.command[7],
        additional_info=job_description.container.command[8],
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
    return {
        format_job_payload(job_description) for job_description in loaded_jobs
    }
