from aioextensions import (
    run,
)
from batch.dal import (
    delete_action,
    get_action,
    update_action_to_dynamodb,
)
from batch_dispatch.clone_roots import (
    clone_roots,
)
from batch_dispatch.handle_finding_policy import (
    handle_finding_policy,
)
from batch_dispatch.move_root import (
    move_root,
)
from batch_dispatch.rebase import (
    rebase,
)
from batch_dispatch.refresh_toe_inputs import (
    refresh_toe_inputs,
)
from batch_dispatch.refresh_toe_lines import (
    refresh_toe_lines,
)
from batch_dispatch.refresh_toe_ports import (
    refresh_toe_ports,
)
from batch_dispatch.remove_group_resources import (
    remove_group_resources,
)
from batch_dispatch.remove_roots import (
    remove_roots,
)
from batch_dispatch.report import (
    report,
)
from batch_dispatch.update_organization_overview import (
    update_organization_overview,
)
from batch_dispatch.update_organization_repositories import (
    update_organization_repositories,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import sys

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
ACTIONS = {
    act.__name__: act
    for act in [  # The action's name must match item.action_name
        clone_roots,
        handle_finding_policy,
        move_root,
        refresh_toe_inputs,
        refresh_toe_lines,
        refresh_toe_ports,
        remove_group_resources,
        remove_roots,
        report,
        update_organization_overview,
        update_organization_repositories,
        rebase,
    ]
}


async def dispatch(action_dynamo_pk: str | None = None) -> None:
    try:
        action_dynamo_pk = action_dynamo_pk or sys.argv[1]

        item = await get_action(
            action_dynamo_pk=action_dynamo_pk,
        )

        if not item:
            LOGGER.exception(
                Exception("No jobs were found"),
                extra={"extra": {"action_dynamo_pk": action_dynamo_pk}},
            )
            return None

        action = item.action_name
        await update_action_to_dynamodb(
            key=item.key, retries=item.retries + 1, running=True
        )

        if action in ACTIONS:
            await ACTIONS[action](item=item)
        else:
            LOGGER.error("Invalid action", extra=dict(extra=locals()))
        await delete_action(dynamodb_pk=item.key)
    except IndexError:
        LOGGER.error("Missing arguments", extra=dict(extra=locals()))

    return None


async def main(action_dynamo_pk: str | None = None) -> None:
    await dynamo_startup()
    try:
        await dispatch(action_dynamo_pk)
    finally:
        await dynamo_shutdown()


if __name__ == "__main__":
    run(main())
