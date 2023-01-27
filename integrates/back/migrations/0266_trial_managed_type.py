# type: ignore

# pylint: disable=invalid-name
"""
migration to set TRIAL to current groups:
- lgray
- integration
- mondtic
- eval

Execution Time:    2022-08-26 at 15:07:56 UTC
Finalization Time: 2022-08-26 at 15:07:57 UTC
"""

from aioextensions import (
    run,
)
from dataloaders import (
    get_new_context,
)
from groups import (
    domain as groups_domain,
)
import logging as log
import logging.config as log_config
from settings import (
    LOGGING,
)
import time

log_config.dictConfig(LOGGING)

LOGGER = log.getLogger(__name__)
LOGGER_CONSOLE = log.getLogger("console")


async def main() -> None:
    loaders = get_new_context()

    groups_name = ["eval", "integration", "lgray", "mondtic"]
    groups_to_migrate = await loaders.group.load_many(groups_name)

    for group in groups_to_migrate:
        new_state = group.state._replace(managed="TRIAL")
        LOGGER_CONSOLE.info(
            group.name, extra={"extra": {"state": group.state}}
        )

        await groups_domain.update_state(
            group_name=group.name,
            state=new_state,
            organization_id=group.organization_id,
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
