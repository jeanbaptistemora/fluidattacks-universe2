#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration aims to fill the organization field for users that do not have
company field or that auto-enrolled to the application.
It will accomplish this by using the organization of the groups these users
have access to.
"""
import aioboto3
from aioextensions import (
    in_thread,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
    Not,
)
import bugsnag
from context import (
    FI_COMMUNITY_PROJECTS,
)
from dynamodb.operations_legacy import (
    RESOURCE_OPTIONS,
)
from group_access.domain import (
    get_user_groups,
)
from groups.domain import (
    get_attributes as get_group_attributes,
)
from organizations.dal import (
    get_by_id as get_organization_attributes,
    get_by_id_old as get_organization_attributes_old,
)
from organizations.domain import (
    get_id_by_name as get_organization_id_by_name,
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

AUTOENROLLED_ORGANIZATION: str = "integrates community"
STAGE: str = os.environ["STAGE"]
USERS_TABLE: str = "FI_users"


async def dynamo_async_scan(
    table: str, scan_attrs: Dict[str, Union[Attr, str]]
) -> List[Dict[str, str]]:
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


async def get_autoenrolled_users() -> List[str]:
    users: List[str] = []
    autoenrolled_org_id: str = await get_organization_id_by_name(
        AUTOENROLLED_ORGANIZATION
    )
    scan_attrs: Dict[str, Union[Attr, str]] = {
        "FilterExpression": Attr("organization").eq(autoenrolled_org_id),
        "ProjectionExpression": "email",
    }
    response_items = await dynamo_async_scan(USERS_TABLE, scan_attrs)
    if response_items:
        users = [item["email"] for item in response_items]
    return users


async def get_users_without_organization() -> List[str]:
    users: List[str] = []
    scan_attrs: Dict[str, Union[Attr, str]] = {
        "FilterExpression": Not(Attr("organization").exists()),
        "ProjectionExpression": "email",
    }
    response_items = await dynamo_async_scan(USERS_TABLE, scan_attrs)
    if response_items:
        users = [item["email"] for item in response_items]
    return users


async def log(message: str) -> None:
    print(message)
    if STAGE != "test":
        await in_thread(bugsnag.notify, Exception(message), "info")


async def main() -> None:
    await log("Starting migration 0013")
    users_without_org: List[str] = await get_users_without_organization()
    autoenrolled_users: List[str] = await get_autoenrolled_users()
    for user in users_without_org + autoenrolled_users:
        projects: List[str] = await get_user_groups(user, True)
        projects = list(
            filter(
                lambda project: project not in FI_COMMUNITY_PROJECTS, projects
            )
        )
        if not projects:
            await log(
                f"----\nUser {user} does not have access to any projects and "
                f"cannot be associated to any organization"
            )
            continue
        org_info: Dict[str, str] = await get_group_attributes(
            projects.pop(0), ["organization"]
        )
        org_id: str = org_info["organization"]
        org_name: Dict[str, str] = await get_organization_attributes_old(
            org_id, ["name"]
        )
        if not org_name.get("name"):
            org_name = await get_organization_attributes(org_id, ["name"])
        if STAGE == "test":
            await log(
                f"----\nUser {user} will be added to the organization "
                f'{org_name.get("name")} with ID {org_id}'
            )
        else:
            await update_user(email=user, data={"organization": org_id})
            await log(
                f"User {user} was added to organization "
                f'{org_name.get("name")}'
            )


if __name__ == "__main__":
    run(main())
