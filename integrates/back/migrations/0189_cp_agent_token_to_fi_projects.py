# pylint: disable=invalid-name
"""
In the context of migrating groups to vms, consolidate data copying the forces
agent token, currently in vms, to the old table with the rest of the data.
This is prior to removing unwanted group items in vms, as the primary key
will change.

Execution Time:    2022-02-21 at 16:35:34 UTC
Finalization Time: 2022-02-21 at 16:37:43 UTC
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from dynamodb.model import (
    get_agent_token,
)
from groups import (
    dal as groups_dal,
    domain as groups_domain,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(
        CustomUnavailabilityError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_group(
    *,
    group_name: str,
    progress: float,
) -> None:
    success = False
    token: Optional[str] = await get_agent_token(group_name=group_name)
    if token:
        success = await groups_dal.update(group_name, {"agent_token": token})
        LOGGER_CONSOLE.info(
            "Group token processed",
            extra={
                "extra": {
                    "group_name": group_name,
                    "token_copied": success,
                    "progress": round(progress, 2),
                }
            },
        )


async def main() -> None:
    group_names = sorted(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    group_names_len = len(group_names)
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "group_names_len": group_names_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                group_name=group_name,
                progress=count / group_names_len,
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=4,
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
