from aioextensions import (
    run,
)
from batch.dal import (
    delete_action,
    get_action,
)
from batch.handle_finding_policy import (
    handle_finding_policy,
)
from batch.handle_virus_scan import (
    handle_virus_scan,
)
from batch.remove_group_resources import (
    remove_group_resources,
)
from batch.report import (
    generate_report,
)
from batch.roots import (
    clone_roots,
    move_root,
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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def main() -> None:  # noqa: MC0001
    try:
        action_dynamo_pk = sys.argv[1]

        item = await get_action(
            action_dynamo_pk=action_dynamo_pk,
        )

        if not item:
            raise Exception(
                f"No jobs were found for the key {action_dynamo_pk}"
            )

        action = item.action_name

        if action == "report":
            await generate_report(item=item)
        elif action == "move_root":
            await move_root(item=item)
        elif action == "handle_finding_policy":
            await handle_finding_policy(item=item)
        elif action == "handle_virus_scan":
            await handle_virus_scan(item=item)
        elif action == "refresh_toe_inputs":
            await refresh_toe_inputs(item=item)
        elif action == "refresh_toe_lines":
            await refresh_toe_lines(item=item)
        elif action == "clone_roots":
            await clone_roots(item=item)
        elif action == "remove_group_resources":
            await remove_group_resources(item=item)
        else:
            LOGGER.error("Invalid action", extra=dict(extra=locals()))
            await delete_action(
                action_name=item.action_name,
                additional_info=item.additional_info,
                entity=item.entity,
                subject=item.subject,
                time=item.time,
            )
    except IndexError:
        LOGGER.error("Missing arguments", extra=dict(extra=locals()))


if __name__ == "__main__":
    run(main())
