# pylint: disable=invalid-name
"""
Remove all machine executions

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
)
import asyncio
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.roots.types import (
    RootMachineExecution,
)
from dynamodb.operations import (
    batch_delete_item,
)
from dynamodb.types import (
    PrimaryKey,
)
from more_itertools import (
    flatten,
)
from organizations.domain import (
    get_all_group_names,
)
import time
from typing import (
    Tuple,
)


async def process_group(loaders: Dataloaders, group_name: str) -> None:
    roots = await loaders.group_roots.load(group_name)
    executions: Tuple[RootMachineExecution, ...] = tuple(
        flatten(
            await loaders.root_machine_executions.load_many(
                [root.id for root in roots]
            )
        )
    )
    keys_to_delete = tuple(
        PrimaryKey(exc.root_id, exc.job_id) for exc in executions
    )
    await batch_delete_item(keys=keys_to_delete, table=TABLE)


async def main() -> None:
    loaders = get_new_context()
    all_groups = await get_all_group_names(loaders)
    await collect(
        [process_group(loaders, group) for group in reversed(all_groups)],
        workers=10,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    asyncio.run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
