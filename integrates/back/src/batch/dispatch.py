from aioextensions import (
    run,
)
from batch.actions.clone_roots import (
    clone_roots,
)
from batch.actions.move_root import (
    move_root,
)
from batch.actions.remove_roots import (
    remove_roots,
)
from batch.dal import (
    delete_action,
    get_action,
    update_action_to_dynamodb,
)
from batch.handle_finding_policy import (
    handle_finding_policy,
)
from batch.remove_group_resources import (
    remove_group_resources,
)
from batch.report import (
    generate_report,
)
from batch.toe_inputs import (
    refresh_toe_inputs,
)
from batch.toe_lines import (
    refresh_toe_lines,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import sys
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger("console")


async def main(action_dynamo_pk: Optional[str] = None) -> None:  # noqa: MC0001
    try:
        action_dynamo_pk = action_dynamo_pk or sys.argv[1]

        item = await get_action(
            action_dynamo_pk=action_dynamo_pk,
        )

        if not item:
            raise Exception(
                f"No jobs were found for the key {action_dynamo_pk}"
            )

        action = item.action_name
        await update_action_to_dynamodb(key=item.key, running=True)

        if action == "report":
            await generate_report(item=item)
        elif action == "move_root":
            await move_root(item=item)
        elif action == "handle_finding_policy":
            await handle_finding_policy(item=item)
        elif action == "refresh_toe_inputs":
            await refresh_toe_inputs(item=item)
        elif action == "refresh_toe_lines":
            await refresh_toe_lines(item=item)
        elif action == "clone_roots":
            await clone_roots(item=item)
        elif action == "remove_group_resources":
            await remove_group_resources(item=item)
        elif action == "remove_roots":
            await remove_roots(item=item)
        else:
            LOGGER.error("Invalid action", extra=dict(extra=locals()))
            await delete_action(dynamodb_pk=item.key)
        await delete_action(dynamodb_pk=item.key)
    except IndexError:
        LOGGER.error("Missing arguments", extra=dict(extra=locals()))


if __name__ == "__main__":
    run(main())
