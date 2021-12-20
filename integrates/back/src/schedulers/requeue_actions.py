from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
    domain as batch_domain,
)
from batch.types import (
    BatchProcessing,
    JobPayload,
)
from typing import (
    List,
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
    action_queues = {
        pending_action.queue for pending_action in pending_actions
    }
    job_payloads = await batch_domain.get_job_payloads(
        queues=list(action_queues),
        statuses=[
            batch_dal.JobStatus.SUBMITTED,
            batch_dal.JobStatus.PENDING,
            batch_dal.JobStatus.RUNNABLE,
            batch_dal.JobStatus.STARTING,
            batch_dal.JobStatus.RUNNING,
        ],
    )
    pending_actions = _filter_refresh_toe_lines_actions(pending_actions)
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
            if JobPayload(
                action_name=action.action_name,
                subject=action.subject,
                entity=action.entity,
                time=action.time,
                additional_info=action.additional_info,
            )
            not in job_payloads
        ],
        workers=20,
    )


async def main() -> None:
    await requeue_actions()
