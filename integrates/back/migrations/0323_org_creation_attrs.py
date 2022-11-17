# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Sets created_by and created_date in org metadata

Execution Time:
Finalization Time:
"""

from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
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


async def process_organization(org_id: str, org_name: str) -> None:
    response = await operations.query(
        condition_expression=(
            Key("pk").eq(org_id) & Key("sk").begins_with("STATE#")
        ),
        facets=(TABLE.facets["organization_historic_state"],),
        table=TABLE,
    )
    historic = response.items
    created_by = historic[0]["modified_by"]
    created_date = historic[0]["modified_date"]
    await operations.update_item(
        item={"created_by": created_by, "created_date": created_date},
        key=PrimaryKey(partition_key=org_id, sort_key=f"ORG#{org_name}"),
        table=TABLE,
    )


async def main() -> None:
    async for organization in orgs_domain.iterate_organizations():
        await process_organization(organization.id, organization.name)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
