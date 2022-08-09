# pylint: disable=invalid-name
"""
Copy roles from authz to access items:
    user    to  stakeholder_metadata
    group   to  group_access_metadata
    org     to  organization_access_metadata

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
import authz
from db_model import (
    group_access as group_access_model,
    organization_access as org_access_model,
    stakeholders as stakeholders_model,
    TABLE,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
)
from db_model.organization_access.types import (
    OrganizationAccessMetadataToUpdate,
)
from db_model.organization_access.utils import (
    remove_org_id_prefix,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
)
from dynamodb import (
    keys,
    operations,
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
AUTHZ_TABLE: str = "fi_authz"

LOWER_CASE_ORG_ID_PREFIX = "org#"
UPPER_CASE_ORG_ID_PREFIX = "ORG#"


def _capitalize_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = organization_id.lstrip(UPPER_CASE_ORG_ID_PREFIX)
    no_prefix_id = organization_id.lstrip(LOWER_CASE_ORG_ID_PREFIX)
    return f"{UPPER_CASE_ORG_ID_PREFIX}{no_prefix_id}"


async def _get_group_access(email: str, group_name: str) -> Item:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": email,
            "name": group_name,
        },
    )
    item = await operations.get_item(
        facets=(TABLE.facets["group_access"],),
        key=primary_key,
        table=TABLE,
    )
    return item


async def _get_organization_access(email: str, organization_id: str) -> Item:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": email,
            "id": remove_org_id_prefix(organization_id),
        },
    )
    item = await operations.get_item(
        facets=(TABLE.facets["organization_access"],),
        key=primary_key,
        table=TABLE,
    )
    return item


async def _get_stakeholder(email: str) -> Item:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    item = await operations.get_item(
        facets=(TABLE.facets["stakeholder_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    return item


async def _grant_group_level_role(
    email: str, group_name: str, role: str
) -> None:
    if role not in authz.get_group_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")
    await group_access_model.update_metadata(
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(role=role),
    )


async def _grant_organization_level_role(
    email: str, organization_id: str, role: str
) -> None:
    if role not in authz.get_organization_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role} - {locals()=}")
    await org_access_model.update_metadata(
        email=email,
        organization_id=organization_id,
        metadata=OrganizationAccessMetadataToUpdate(role=role),
    )


async def _grant_user_level_role(email: str, role: str) -> None:
    if role not in authz.get_user_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")
    await stakeholders_model.update_metadata(
        email=email,
        metadata=StakeholderMetadataToUpdate(role=role),
    )


async def process_authz_policy(item: Item) -> None:
    policy_level = item["level"]
    email = item["subject"]
    policy_object = item["object"]
    role = item["role"]

    if policy_level == "group":
        group_name = policy_object
        if not await _get_group_access(email=email, group_name=group_name):
            return
        await _grant_group_level_role(email, group_name, role)

    elif policy_level == "organization":
        organization_id = _capitalize_org_id_prefix(policy_object)
        if not await _get_organization_access(
            email=email,
            organization_id=organization_id,
        ):
            return
        await _grant_organization_level_role(email, organization_id, role)

    elif policy_level == "user":
        if not await _get_stakeholder(email=email):
            return
        await _grant_user_level_role(email, role)

    else:
        raise ValueError(f"Invalid level value: {policy_level=}")

    LOGGER_CONSOLE.info(
        "Processed",
        extra={"extra": {"policy": item}},
    )


async def main() -> None:
    items: list[Item] = await ops_legacy.scan(table=AUTHZ_TABLE, scan_attrs={})
    LOGGER_CONSOLE.info(
        "Authz policies scanned",
        extra={"extra": {"scanned": len(items)}},
    )

    await collect(
        (process_authz_policy(item) for item in items),
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
