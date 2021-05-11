
import logging
import logging.config
import sys

from aioextensions import run

from back.settings import LOGGING
from batch.dal import (
    delete_action,
    get_action,
)
from batch.report import generate_report
from batch.roots import move_root


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def main() -> None:
    try:
        action = sys.argv[1]
        subject = sys.argv[2]
        entity = sys.argv[3]
        time = sys.argv[4]
        additional_info = sys.argv[5]

        item = await get_action(
            action_name=action,
            additional_info=additional_info,
            entity=entity,
            subject=subject,
            time=time,
        )
        if not item:
            return
        if action == 'report' and additional_info in {'PDF', 'XLS', 'DATA'}:
            await generate_report(item=item)
        elif action == 'move_root':
            await move_root(item=item)
        else:
            LOGGER.error('Invalid action', extra=dict(extra=locals()))
            await delete_action(
                action_name=item.action_name,
                additional_info=item.additional_info,
                entity=item.entity,
                subject=item.subject,
                time=item.time,
            )
    except IndexError:
        LOGGER.error('Missing arguments', extra=dict(extra=locals()))


if __name__ == '__main__':
    run(main())
