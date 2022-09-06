# pylint: disable=invalid-name
"""
Sets created_by and created_date in group metadata

Execution Time:    2022-09-06 at 14:34:08 UTC
Finalization Time: 2022-09-06 at 14:35:20 UTC
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
    TABLE,
)
from db_model.groups.types import (
    GroupState,
)
from dynamodb import (
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
import logging
import logging.config
from organizations.domain import (
    iterate_organizations_and_groups,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def process_group(
    loaders: Dataloaders, group_name: str, org_id: str
) -> None:
    historic: tuple[GroupState, ...] = await loaders.group_historic_state.load(
        group_name
    )
    created_by = historic[0].modified_by
    created_date = historic[0].modified_date
    await operations.update_item(
        item={"created_by": created_by, "created_date": created_date},
        key=PrimaryKey(partition_key=f"GROUP#{group_name}", sort_key=org_id),
        table=TABLE,
    )


async def main() -> None:
    loaders = get_new_context()
    async for org_id, _, org_group_names in iterate_organizations_and_groups(
        loaders
    ):
        await collect(
            process_group(loaders, group_name, org_id)
            for group_name in org_group_names
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
