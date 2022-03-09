from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    JobStatus,
    Product,
)
from batch.types import (
    BatchProcessing,
)
from typing import (
    List,
    NamedTuple,
)


class CompleteBatchJob(NamedTuple):
    id: str
    status: JobStatus
    vcpus: int


async def _get_machine_keys_to_delete(
    running_actions: List[BatchProcessing],
    complete_batch_jobs: List[CompleteBatchJob],
) -> List[str]:
    # Machine executions may fail due to memory consumption.
    # If there is a failed job, requeue the execution using more resources.
    # If it still fails, delete it from the DB or else it will be requeued
    # indefinitely
    machine_actions_to_retry: List[BatchProcessing] = [
        action
        for action in running_actions
        if action.action_name == Action.EXECUTE_MACHINE.value
        for batch_job in complete_batch_jobs
        if action.batch_job_id == batch_job.id
        and batch_job.status == JobStatus.FAILED
        and batch_job.vcpus <= 4
    ]
    await collect(
        batch_dal.put_action(
            action=Action.EXECUTE_MACHINE,
            additional_info=action.additional_info,
            attempt_duration_seconds=86400,
            entity=action.entity,
            memory=15400,
            product_name=Product.SKIMS,
            queue=action.queue,
            subject=action.subject,
            vcpus=8,
        )
        for action in machine_actions_to_retry
    )

    machine_keys_to_delete: List[str] = [
        action.key
        for action in running_actions
        if action.action_name == Action.EXECUTE_MACHINE.value
        for batch_job in complete_batch_jobs
        if action.batch_job_id == batch_job.id
        and batch_job.status == JobStatus.FAILED
    ]
    return machine_keys_to_delete


async def _filter_active_and_completed_actions(
    actions_to_requeue: List[BatchProcessing],
) -> List[BatchProcessing]:
    # Deletes entries from the DB that have a complete Batch execution
    # with status SUCCEEDED and for whatever reason remain in the DB.
    running_actions: List[BatchProcessing] = [
        action
        for action in actions_to_requeue
        if action.running and action.batch_job_id
    ]
    batch_jobs: List[CompleteBatchJob] = [
        CompleteBatchJob(
            id=str(job["jobId"]),
            status=JobStatus(job["status"]),
            vcpus=int(job["container"]["vcpus"]),
        )
        for job in await batch_dal.describe_jobs(
            *[
                action.batch_job_id
                for action in running_actions
                if action.batch_job_id is not None  # Check to comply with Mypy
            ]
        )
    ]

    succeeded_keys_to_delete: List[str] = [
        action.key
        for action in running_actions
        for batch_job in batch_jobs
        if action.batch_job_id == batch_job.id
        and batch_job.status == JobStatus.SUCCEEDED
    ]
    machine_keys_to_delete: List[str] = await _get_machine_keys_to_delete(
        running_actions, batch_jobs
    )
    keys_to_delete: List[str] = (
        succeeded_keys_to_delete + machine_keys_to_delete
    )
    await collect(
        [batch_dal.delete_action(dynamodb_pk=key) for key in keys_to_delete]
    )

    active_keys: List[str] = [
        action.key
        for action in running_actions
        for batch_job in batch_jobs
        if action.batch_job_id == batch_job.id
        and batch_job.status not in {JobStatus.FAILED, JobStatus.SUCCEEDED}
    ]

    return [
        action
        for action in actions_to_requeue
        if action.key not in set(active_keys + keys_to_delete)
    ]


def _filter_duplicated_actions(
    actions_to_requeue: List[BatchProcessing], action_to_filter: Action
) -> List[BatchProcessing]:
    # Prevents that entries with the same action over the same entity
    # are requeued at the same time
    filtered_unique_actions: List[BatchProcessing] = list(
        {
            action.entity: action
            for action in actions_to_requeue
            if action.action_name == action_to_filter.value
        }.values()
    )
    remaining_actions: List[BatchProcessing] = [
        action
        for action in actions_to_requeue
        if action.action_name != action_to_filter.value
    ]
    return filtered_unique_actions + remaining_actions


async def requeue_actions() -> bool:
    actions_to_requeue: List[BatchProcessing] = await batch_dal.get_actions()
    actions_to_requeue = _filter_duplicated_actions(
        actions_to_requeue, Action.REFRESH_TOE_INPUTS
    )
    actions_to_requeue = _filter_duplicated_actions(
        actions_to_requeue, Action.REFRESH_TOE_LINES
    )
    actions_to_requeue = await _filter_active_and_completed_actions(
        actions_to_requeue
    )

    report_additional_info = dict(
        vcpus=4,
        attempt_duration_seconds=7200,
    )
    new_batch_jobs_ids = await collect(
        (
            batch_dal.put_action_to_batch(
                action_name=action.action_name,
                action_dynamo_pk=action.key,
                entity=action.entity,
                queue=action.queue,
                product_name=(
                    Product.SKIMS
                    if action.action_name == "execute-machine"
                    else Product.INTEGRATES
                ).value,
                **(
                    report_additional_info
                    if action.action_name == "report"
                    else {}
                ),
            )
            for action in actions_to_requeue
        ),
        workers=20,
    )
    return all(
        await collect(
            (
                batch_dal.update_action_to_dynamodb(
                    key=action.key, batch_job_id=job_id, running=None
                )
                for action, job_id in zip(
                    actions_to_requeue, new_batch_jobs_ids
                )
            ),
            workers=20,
        )
    )


async def main() -> None:
    await requeue_actions()
