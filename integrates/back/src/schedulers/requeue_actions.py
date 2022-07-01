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
    Any,
    NamedTuple,
)


class CompleteBatchJob(NamedTuple):
    id: str
    status: JobStatus
    vcpus: int


async def _get_machine_keys_to_delete(
    running_actions: list[BatchProcessing],
    complete_batch_jobs: list[dict[str, Any]],
) -> list[str]:
    # Machine executions may fail due to memory consumption.
    # If there is a failed job, requeue the execution using more resources.
    # If it still fails, delete it from the DB or else it will be requeued
    # indefinitely

    machine_keys_to_delete: list[str] = [
        action.key
        for action in running_actions
        if action.action_name == Action.EXECUTE_MACHINE.value
        for batch_job in complete_batch_jobs
        if action.batch_job_id == batch_job["jobId"]
        and batch_job["status"] == JobStatus.FAILED.value
    ]
    return machine_keys_to_delete


async def _filter_non_requeueable_actions(
    actions_to_requeue: list[BatchProcessing],
) -> list[BatchProcessing]:
    """Filters actions that should not be sent to Batch"""
    batch_jobs_dict: dict[str, dict[str, Any]] = {
        job["jobId"]: job
        for job in await batch_dal.describe_jobs(
            *[
                action.batch_job_id
                for action in actions_to_requeue
                if action.batch_job_id is not None  # Check to comply with Mypy
            ]
        )
    }

    succeeded_keys_to_delete: list[str] = [
        action.key
        for action in actions_to_requeue
        if action.batch_job_id
        if (
            batch_jobs_dict.get(action.batch_job_id, {"status": None})[
                "status"
            ]
            == "SUCCEEDED"
        )
        # remove false positives jobs failed
        or (
            batch_jobs_dict.get(action.batch_job_id, {"status": None})[
                "status"
            ]
            == "FAILED"
            and (
                # canceled jobs
                "stoppedAt" not in batch_jobs_dict[action.batch_job_id]
                # false positive, the job has status FAILED but make ends
                # in success
                or "CannotInspectContainerError"
                in batch_jobs_dict[action.batch_job_id]["container"].get(
                    "reason", ""
                )
            )
        )
    ]
    succeeded_keys_to_delete = [
        *succeeded_keys_to_delete,
        *(
            await _get_machine_keys_to_delete(
                [action for action in actions_to_requeue if action.running],
                list(batch_jobs_dict.values()),
            )
        ),
    ]

    await collect(
        [
            batch_dal.delete_action(dynamodb_pk=key)
            for key in succeeded_keys_to_delete
        ]
    )

    active_keys: list[str] = [
        action.key
        for action in actions_to_requeue
        if action.running
        and action.batch_job_id
        and batch_jobs_dict.get(action.batch_job_id, {"status": None})[
            "status"
        ]
        in [
            "RUNNING",
        ]
    ]
    pending_keys: list[str] = [
        action.key
        for action in actions_to_requeue
        if not action.running
        and action.batch_job_id
        and batch_jobs_dict.get(action.batch_job_id, {"status": None})[
            "status"
        ]
        in {
            "SUBMITTED",
            "PENDING",
            "RUNNABLE",
            "STARTING",
            "RUNNING",  # makes setup
        }
    ]

    return [
        action
        for action in actions_to_requeue
        if action.key
        not in set(active_keys + pending_keys + succeeded_keys_to_delete)
    ]


def _filter_duplicated_actions(
    actions_to_requeue: list[BatchProcessing], action_to_filter: Action
) -> list[BatchProcessing]:
    # Prevents that entries with the same action over the same entity
    # are requeued at the same time
    filtered_unique_actions: list[BatchProcessing] = list(
        {
            action.entity: action
            for action in actions_to_requeue
            if action.action_name == action_to_filter.value
        }.values()
    )
    remaining_actions: list[BatchProcessing] = [
        action
        for action in actions_to_requeue
        if action.action_name != action_to_filter.value
    ]
    return filtered_unique_actions + remaining_actions


async def requeue_actions() -> bool:
    actions_to_requeue: list[BatchProcessing] = await batch_dal.get_actions()
    actions_to_requeue = _filter_duplicated_actions(
        actions_to_requeue, Action.REFRESH_TOE_INPUTS
    )
    actions_to_requeue = _filter_duplicated_actions(
        actions_to_requeue, Action.REFRESH_TOE_LINES
    )
    actions_to_requeue = await _filter_non_requeueable_actions(
        actions_to_requeue
    )

    batch_jobs_dict: dict[str, dict[str, Any]] = {
        job["jobId"]: job
        for job in await batch_dal.describe_jobs(
            *[
                action.batch_job_id
                for action in actions_to_requeue
                if action.batch_job_id is not None
            ]
        )
    }
    futures = []
    attempt_duration_seconds: int = 3600
    for action in actions_to_requeue:
        if action.action_name == "execute-machine":
            continue
        if action.batch_job_id:
            if action.batch_job_id in batch_jobs_dict:
                try:
                    resources = {
                        res["type"]: int(res["value"])
                        for res in batch_jobs_dict[action.batch_job_id][
                            "container"
                        ]["resourceRequirements"]
                    }
                    vcpus = resources["VCPU"]
                    memory = resources["MEMORY"]
                    attempt_duration_seconds = batch_jobs_dict[
                        action.batch_job_id
                    ]["timeout"]["attemptDurationSeconds"]
                except KeyError:
                    vcpus = 2
                    memory = 2
            else:
                vcpus = 2
                memory = 2
            futures.append(
                batch_dal.put_action_to_batch(
                    action_name=action.action_name,
                    attempt_duration_seconds=attempt_duration_seconds,
                    action_dynamo_pk=action.key,
                    entity=action.entity,
                    queue=action.queue,
                    product_name=Product.INTEGRATES.value,
                    memory=memory,
                    vcpus=vcpus,
                )
            )
    new_batch_jobs_ids = await collect(
        futures,
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
