# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Migrate forces executions to "integrates_vms" table.

Execution Time:    2022-09-05 at 15:10:34 UTC
Finalization Time: 2022-09-05 at 15:18:16 UTC
"""

from aioextensions import (
    collect,
    run,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    ExecutionAlreadyCreated,
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
import logging
import logging.config
from newutils.forces import (
    format_forces,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
FORCES_TABLE = "FI_forces"


async def process_execution(item: Item) -> None:
    forces_execution: ForcesExecution = format_forces(item)
    with suppress(ExecutionAlreadyCreated):
        await forces_model.add(forces_execution=forces_execution)


async def main() -> None:
    executions_scanned: list[Item] = await ops_legacy.scan(
        table=FORCES_TABLE, scan_attrs={}
    )
    LOGGER_CONSOLE.info(
        "All forces executions",
        extra={"extra": {"scanned": len(executions_scanned)}},
    )

    await collect(
        tuple(process_execution(item) for item in executions_scanned),
        workers=256,
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
