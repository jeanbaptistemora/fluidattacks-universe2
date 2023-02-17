# pylint: disable=invalid-name
"""
Confirm already completed invation registration

Execution Time:    2023-02-17 at 22:48:54 UTC
Finalization Time: 2023-02-17 at 22:57:32 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    timedelta,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessRequest,
)
from groups.domain import (
    complete_register_for_group_invitation,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(group_name: str) -> None:
    loaders: Dataloaders = get_new_context()
    stakeholders_access = await loaders.group_stakeholders_access.load(
        group_name
    )
    for access in stakeholders_access:
        if access.invitation and not access.invitation.is_used:
            historic_access: list[GroupAccess] = list(
                await loaders.group_historic_access.load(
                    GroupAccessRequest(
                        email=access.email, group_name=group_name
                    )
                )
            )[-2:]
            if len(historic_access) > 1:
                if (
                    historic_access[1].invitation
                    and not historic_access[1].invitation.is_used
                ) and (
                    historic_access[0].invitation
                    and historic_access[0].invitation.is_used
                ):
                    if (
                        historic_access[1].state.modified_date is not None
                        and historic_access[0].state.modified_date is not None
                        and abs(
                            historic_access[1].state.modified_date
                            - historic_access[0].state.modified_date
                        )
                        < timedelta(seconds=1)
                    ):
                        await complete_register_for_group_invitation(
                            loaders=get_new_context(), group_access=access
                        )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    count = 0
    LOGGER_CONSOLE.info(
        "All group names",
        extra={
            "extra": {
                "total": len(all_group_names),
            }
        },
    )
    for group_name in all_group_names:
        count += 1
        LOGGER_CONSOLE.info(
            "Group",
            extra={
                "extra": {
                    "group_name": group_name,
                    "count": count,
                }
            },
        )
        await process_group(group_name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
