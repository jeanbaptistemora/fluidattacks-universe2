from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Product,
)
from batch.types import (
    BatchProcessing,
)
from typing import (
    List,
)


def _filter_refresh_toe_inputs_actions(
    pending_actions: List[BatchProcessing],
) -> List[BatchProcessing]:
    refresh_toe_inputs_actions_to_requeue = list(
        {
            action.entity: action
            for action in pending_actions
            if action.action_name == "refresh_toe_inputs"
        }.values()
    )
    non_refresh_toe_inputs_actions = [
        action
        for action in pending_actions
        if not action.action_name == "refresh_toe_inputs"
    ]
    return (
        non_refresh_toe_inputs_actions + refresh_toe_inputs_actions_to_requeue
    )


def _filter_refresh_toe_lines_actions(
    pending_actions: List[BatchProcessing],
) -> List[BatchProcessing]:
    refresh_toe_lines_actions_to_requeue = list(
        {
            action.entity: action
            for action in pending_actions
            if action.action_name == "refresh_toe_lines"
        }.values()
    )
    non_refresh_toe_lines_actions = [
        action
        for action in pending_actions
        if not action.action_name == "refresh_toe_lines"
    ]
    return non_refresh_toe_lines_actions + refresh_toe_lines_actions_to_requeue


async def requeue_actions() -> None:
    pending_actions: List[BatchProcessing] = await batch_dal.get_actions()
    removable_actions = {"execute-machine"}

    pending_actions = _filter_refresh_toe_inputs_actions(pending_actions)
    pending_actions = _filter_refresh_toe_lines_actions(pending_actions)
    report_additional_info = dict(
        vcpus=4,
        attempt_duration_seconds=7200,
    )
    running_actions = [action for action in pending_actions if action.running]
    # jobs that are running in the db but failed in batch
    failed_batch_job: List[str] = [
        job["jobId"]
        for job in await batch_dal.describe_jobs(
            *[
                action.batch_job_id
                for action in running_actions
                if action.batch_job_id
            ]
        )
        if job["status"]
        in [
            batch_dal.JobStatus.FAILED.value,
            batch_dal.JobStatus.SUCCEEDED.value,
        ]
    ]
    # remove actions that in their normal process can fail
    removed_actions_key = [
        action.key
        for action in pending_actions
        if action.action_name in removable_actions
        and (
            action.batch_job_id is not None
            and action.batch_job_id in failed_batch_job
        )
    ]
    await collect(
        [
            batch_dal.delete_action(dynamodb_pk=action_key)
            for action_key in removed_actions_key
        ]
    )
    await collect(
        [
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
            for action in pending_actions
            if (
                action.key not in removed_actions_key
                and action.batch_job_id is not None
                and action.batch_job_id in failed_batch_job
            )
        ],
        workers=20,
    )


async def main() -> None:
    await requeue_actions()
