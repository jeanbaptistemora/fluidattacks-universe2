#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration aims to delete all the duplicate organizations that were
created for the organization 'Integrates Community' while the method
'get or create' was case-sensitive.
It leaves only one and changes the ID in all the users of duplicated
organizations
"""
import aioboto3
from aioextensions import (
    collect,
    in_thread,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
import bugsnag
from dynamodb.operations_legacy import (
    RESOURCE_OPTIONS,
)
import os
from typing import (
    Dict,
    List,
    Union,
)
from users.dal import (
    update as update_user,
)

INTEGRATES_TABLE = "integrates"
ORGANIZATION_NAME = "integrates community"
ORGANIZATIONS_TABLE = "fi_organizations"
STAGE: str = os.environ["STAGE"]
USERS_TABLE = "FI_users"

OrgsUsersType = List[Dict[str, List[str]]]


async def dynamo_delete_item(
    table: str, delete_attrs: Dict[str, Dict[str, str]]
) -> bool:
    success = False
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.delete_item(**delete_attrs)
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    return success


async def dynamo_async_scan(
    table: str, scan_attrs: Dict[str, Union[Key, str]]
) -> List[Dict[str, str]]:
    # pylint: disable=unsubscriptable-object
    response_items: List[Dict[str, str]] = []
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.scan(**scan_attrs)
        response_items += response.get("Items", [])
        while response.get("LastEvaluatedKey"):
            scan_attrs.update(
                {"ExclusiveStartKey": response.get("LastEvaluatedKey")}
            )
            response = await dynamo_table.scan(**scan_attrs)
            response_items += response["Items"]
    return response_items


async def get_organization_ids_by_name(org_name: str) -> List[str]:
    organization_ids: List[str] = []
    scan_attrs = {
        "FilterExpression": Attr("sk").eq(org_name),
        "IndexName": "gsi-1",
        "ProjectionExpression": "pk",
    }
    response_items = await dynamo_async_scan(INTEGRATES_TABLE, scan_attrs)
    if response_items:
        organization_ids = [item["pk"] for item in response_items]
    return organization_ids


async def get_users_by_organizations(org_ids: List[str]) -> OrgsUsersType:
    orgs_users: OrgsUsersType = []
    response_items = await collect(
        dynamo_async_scan(
            USERS_TABLE,
            {
                "FilterExpression": Attr("organization").eq(org_id),
                "ProjectionExpression": "email",
            },
        )
        for org_id in org_ids
    )
    for index, users in enumerate(response_items):
        orgs_users.append({org_ids[index]: [user["email"] for user in users]})
    return orgs_users


async def log(msg: str) -> None:
    print(msg)
    if STAGE != "test":
        await in_thread(bugsnag.notify, Exception(msg), "info")


async def main() -> None:
    await log("Starting migration 0012")
    org_ids: List[str] = await get_organization_ids_by_name(ORGANIZATION_NAME)
    unique_org_id: str = org_ids.pop(0)
    orgs_users: OrgsUsersType = await get_users_by_organizations(org_ids)
    await log(
        f'Unique "Integrates Community" organization will have ID '
        f"{unique_org_id}"
    )
    for org_users in orgs_users:
        for org, users in org_users.items():
            await migrate_organization_users(org, users, unique_org_id)


async def migrate_organization_users(
    old_org_id: str, users: List[str], new_org_id: str
) -> bool:
    success: bool = False
    if STAGE == "test":
        await log(
            f"----\nUsers with organization {old_org_id} will be migrated"
        )
        for user in users:
            await log(f"Organization will be updated for user {user}")
    else:
        results = await collect(
            update_user(email=user, data={"organization": new_org_id})
            for user in users
        )

        success = all(results)
        if success:
            delete_attrs = {"Key": {"pk": old_org_id, "sk": ORGANIZATION_NAME}}
            await dynamo_delete_item(INTEGRATES_TABLE, delete_attrs)
            await dynamo_delete_item(ORGANIZATIONS_TABLE, delete_attrs)
            await log(
                f"Organization ID was updated from {old_org_id} to "
                f'{new_org_id} for the users: {", ".join(users)}'
            )
    return success


if __name__ == "__main__":
    run(main())
