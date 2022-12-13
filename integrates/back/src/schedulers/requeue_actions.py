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
import logging
from typing import (
    Any,
    NamedTuple,
)

# Constants
LOGGER = logging.getLogger(__name__)


class CompleteBatchJob(NamedTuple):
    id: str
    status: JobStatus
    vcpus: int


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
    retried_keys_to_delete = []
    for action in actions_to_requeue:
        if action.retries > 3:
            retried_keys_to_delete.append(action.key)
            LOGGER.error(
                "Batch action exceeded number of retries",
                extra={
                    "extra": {
                        "action_name": action.action_name,
                        "entity": action.entity,
                        "last_batch_job": action.batch_job_id,
                        "addition_info": action.additional_info,
                    }
                },
            )

    keys_to_delete = [*succeeded_keys_to_delete, *retried_keys_to_delete]

    await collect(
        [batch_dal.delete_action(dynamodb_pk=key) for key in keys_to_delete]
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
        if action.key not in set(active_keys + pending_keys + keys_to_delete)
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
    actions_to_requeue = _filter_duplicated_actions(
        actions_to_requeue, Action.REFRESH_TOE_PORTS
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
    for action in actions_to_requeue:
        if action.batch_job_id:
            kwargs = {}
            if action.batch_job_id in batch_jobs_dict:
                try:
                    vcpus = batch_jobs_dict[action.batch_job_id]["container"][
                        "vcpus"
                    ]
                    memory = batch_jobs_dict[action.batch_job_id]["container"][
                        "memory"
                    ]
                    kwargs.update({"memory": memory, "vcpus": vcpus})
                except KeyError:
                    if action.action_name == Action.EXECUTE_MACHINE.value:
                        kwargs = {"memory": 7200, "vcpus": 4}
            product = (
                Product.INTEGRATES
                if action.action_name != Action.EXECUTE_MACHINE.value
                else Product.SKIMS
            )
            futures.append(
                batch_dal.put_action_to_batch(
                    action_name=action.action_name,
                    attempt_duration_seconds=(
                        43200
                        if action.action_name == Action.EXECUTE_MACHINE.value
                        else 3600
                    ),
                    action_dynamo_pk=action.key,
                    entity=action.entity,
                    queue=batch_dal.to_queue(action.queue, product),
                    product_name=product.value,
                    **kwargs,
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
