# type: ignore

# pylint: disable=invalid-name
"""
Migrate stakeholder organization access to "integrates_vms" table.
This info is currently in "fi_organizations".

Execution Time:    2022-07-26 at 00:58:42 UTC
Finalization Time: 2022-07-26 at 00:58:52 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    organization_access as orgs_access_model,
    organizations as orgs_model,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
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
    organization_access as org_access_utils,
    organizations as orgs_utils,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
ORGANIZATIONS_TABLE = "fi_organizations"


async def get_users_access_items(organization_id: str) -> list[Item]:
    organization_id = orgs_utils.remove_org_id_prefix(organization_id)
    query_attrs = {
        "KeyConditionExpression": (
            Key("pk").eq(f"ORG#{organization_id}")
            & Key("sk").begins_with("USER#")
        )
    }
    return await ops_legacy.query(ORGANIZATIONS_TABLE, query_attrs)


async def process_org_access(item: Item) -> None:
    org_access: OrganizationAccess = (
        org_access_utils.format_organization_access(item)
    )
    await orgs_access_model.add(organization_access=org_access)


async def process_organization(organization: Organization) -> None:
    access_items = await get_users_access_items(organization.id)
    await collect(process_org_access(item) for item in access_items)

    LOGGER_CONSOLE.info(
        "Processed",
        extra={
            "extra": {
                "org_id": organization.id,
                "org_name": organization.name,
                "access_items": len(access_items),
            }
        },
    )


async def main() -> None:
    all_asm_orgs = await orgs_model.get_all_organizations()
    active_orgs = [
        org
        for org in all_asm_orgs
        if org.state.status == OrganizationStateStatus.ACTIVE
    ]

    LOGGER_CONSOLE.info(
        "Active organizations",
        extra={"extra": {"scanned": len(active_orgs)}},
    )

    await collect(
        tuple(process_organization(org) for org in active_orgs),
        workers=16,
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
