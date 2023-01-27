# pylint: disable=invalid-name
"""
Drops the last state for groups that were already deleted
To ammend a mistake in a previous migration

Execution Time:    2022-09-07 at 15:14:07 UTC
Finalization Time: 2022-09-07 at 15:15:11 UTC
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
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
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
import simplejson as json
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def process_group(
    loaders: Dataloaders, group_name: str, org_id: str
) -> None:
    group: Group = await loaders.group.load(group_name)

    if group.state.status == GroupStateStatus.DELETED:
        historic = await loaders.group_historic_state.load(group_name)
        if historic[-2].status == GroupStateStatus.DELETED:
            LOGGER.info("Fixing %s", group.name)
            await operations.update_item(
                item={"state": json.loads(json.dumps(historic[-2]))},
                key=PrimaryKey(
                    partition_key=f"GROUP#{group_name}", sort_key=org_id
                ),
                table=TABLE,
            )
            await operations.delete_item(
                key=PrimaryKey(
                    partition_key=f"GROUP#{group_name}",
                    sort_key=f"STATE#{group.state.modified_date}",
                ),
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
