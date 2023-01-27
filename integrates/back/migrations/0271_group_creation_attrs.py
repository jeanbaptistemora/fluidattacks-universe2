# pylint: disable=invalid-name
"""
Sets created_by and created_date in group metadata

Execution Time:    2022-09-06 at 14:34:08 UTC
Finalization Time: 2022-09-06 at 14:35:20 UTC

Execution Time:    2022-09-16 at 19:49:31 UTC
Finalization Time: 2022-09-16 at 19:53:59 UTC
"""

from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
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
from organizations import (
    domain as orgs_domain,
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
    historic: list[GroupState] = await loaders.group_historic_state.load(
        group_name
    )
    created_by = historic[0].modified_by
    created_date = historic[0].modified_date
    key_structure = TABLE.primary_key
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item={"created_by": created_by, "created_date": created_date},
        key=PrimaryKey(partition_key=f"GROUP#{group_name}", sort_key=org_id),
        table=TABLE,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_organization_ids = {"ORG#unknown"}
    async for organization in orgs_domain.iterate_organizations():
        all_organization_ids.add(organization.id)

    for organization_id in all_organization_ids:
        group_names = await orgs_domain.get_group_names(
            loaders, organization_id
        )
        for group_name in group_names:
            print("group_name", group_name)
            await process_group(loaders, group_name, organization_id)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
