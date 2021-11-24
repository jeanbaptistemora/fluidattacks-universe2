from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.types import (
    BatchProcessing,
)
from typing import (
    List,
)


async def requeue_actions() -> None:
    pending_actions: List[BatchProcessing] = await batch_dal.get_actions()
    action_queues = {
        pending_action.queue for pending_action in pending_actions
    }
    queues_jobs = await batch_dal.list_queues_jobs(
        queues=list(action_queues),
        statuses=[
            batch_dal.JobStatus.SUBMITTED,
            batch_dal.JobStatus.PENDING,
            batch_dal.JobStatus.RUNNABLE,
            batch_dal.JobStatus.STARTING,
            batch_dal.JobStatus.RUNNING,
        ],
    )
    non_executed_jobs = await batch_dal.decribe_jobs(
        set(queues_jobs.id for queues_jobs in queues_jobs)
    )
    non_executed_jobs_info = {
        (
            job_description.container.command[4],  # action_name
            job_description.container.command[5],  # subject
            job_description.container.command[6],  # entity
            job_description.container.command[7],  # time
            job_description.container.command[8],  # additional_info
        )
        for job_description in non_executed_jobs
    }
    await collect(
        [
            batch_dal.put_action_to_batch(
                action_name=action.action_name,
                entity=action.entity,
                subject=action.subject,
                time=action.time,
                additional_info=action.additional_info,
                queue=action.queue,
            )
            for action in pending_actions
            if (
                action.action_name,
                action.subject,
                action.entity,
                action.time,
                action.additional_info,
            )
            not in non_executed_jobs_info
        ],
        workers=20,
    )


async def main() -> None:
    await requeue_actions()
