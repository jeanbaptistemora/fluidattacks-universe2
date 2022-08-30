# pylint: disable=invalid-name
"""
Migrate forces executions to "integrates_vms" table.
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    forces as forces_model,
)
from db_model.forces.types import (
    ForcesExecution,
)
from dynamodb import (
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils.forces import (
    format_forces,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
FORCES_TABLE = "FI_forces"


async def process_execution(
    loaders: Any, all_active_group_names: tuple[str, ...], item: Item
) -> None:
    group_name = item["subscription"]
    if (
        not await groups_domain.exists(loaders, group_name)
        or group_name not in all_active_group_names
    ):
        return
    forces_execution: ForcesExecution = format_forces(item)
    await forces_model.add(forces_execution=forces_execution)


async def main() -> None:
    loaders = get_new_context()
    executions_scanned: list[Item] = await ops_legacy.scan(
        table=FORCES_TABLE, scan_attrs={}
    )
    all_active_group_names = await orgs_domain.get_all_active_group_names(
        loaders
    )
    LOGGER_CONSOLE.info(
        "All forces executions",
        extra={"extra": {"scanned": len(executions_scanned)}},
    )

    await collect(
        tuple(
            process_execution(loaders, all_active_group_names, item)
            for item in executions_scanned
        ),
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
