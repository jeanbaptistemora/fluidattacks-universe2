# Standard libraries

# Third-party libraries
from aioextensions import collect

# Local libraries
from batch import dal as batch_dal


async def requeue_actions() -> None:
    pending_actions = await batch_dal.get_actions()
    await collect(
        [
            batch_dal.put_action_to_batch(
                action_name=action.action_name,
                entity=action.entity,
                subject=action.subject,
                time=action.time,
                additional_info=action.additional_info,
            )
            for action in pending_actions
        ],
        workers=20
    )


async def main() -> None:
    await requeue_actions()
