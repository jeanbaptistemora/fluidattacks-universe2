# pylint: disable=invalid-name
"""
Add a default value for sprint_start_date

Execution Time:    2022-06-08 at 22:29:29 UTC
Finalization Time: 2022-06-08 at 22:30:44 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
    GroupMetadataToUpdate,
)
from db_model.utils import (
    get_first_day_iso_date,
)
from groups.domain import (
    update_metadata,
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
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(
    *,
    group: Group,
    progress: float,
) -> None:
    if group.sprint_start_date == get_first_day_iso_date():
        await update_metadata(
            group_name=group.name,
            metadata=GroupMetadataToUpdate(
                sprint_start_date=get_first_day_iso_date()
            ),
            organization_id=group.organization_id,
        )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group.name,
                "organization_id": group.organization_id,
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_groups(loaders)
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"groups_len": len(active_groups)}},
    )

    await collect(
        tuple(
            process_group(
                group=group,
                progress=count / len(active_groups),
            )
            for count, group in enumerate(active_groups)
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
