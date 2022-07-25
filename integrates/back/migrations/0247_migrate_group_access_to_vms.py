# pylint: disable=invalid-name
"""
Migrate stakeholder group access to "integrates_vms" table.
This info is currently in "FI_project_access".

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    group_access as group_access_model,
)
from dynamodb import (
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils import (
    group_access as group_access_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
PROJECT_ACCESS_TABLE = "FI_project_access"


async def process_group_access_item(item: Item) -> None:
    group_access = group_access_utils.format_group_access(item)
    await group_access_model.add(group_access=group_access)

    LOGGER_CONSOLE.info(
        "Processed",
        extra={
            "extra": {
                "email": group_access.email,
                "group_name": group_access.group_name,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    active_group_names = await orgs_domain.get_all_active_group_names(loaders)
    LOGGER_CONSOLE.info(
        "Active groups",
        extra={"extra": {"names": len(active_group_names)}},
    )

    group_access_scanned: list[Item] = await ops_legacy.scan(
        table=PROJECT_ACCESS_TABLE, scan_attrs={}
    )
    group_access_filtered: list[Item] = [
        item
        for item in group_access_scanned
        if item["project_name"] in active_group_names
    ]
    LOGGER_CONSOLE.info(
        "Group access items",
        extra={
            "extra": {
                "scanned": len(group_access_scanned),
                "to_process": len(group_access_filtered),
            }
        },
    )

    await collect(
        tuple(
            process_group_access_item(item) for item in group_access_filtered
        ),
        workers=32,
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
