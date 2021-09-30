#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration populates the organization table with the name, users and
groups that belong to that organization.

Execution Time: 2020-06-30 10:50 UTC-5
Finalization Time: 2020-06-30 11:03 UTC-5
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
from botocore.exceptions import (
    ClientError,
)
import bugsnag
from dynamodb.operations_legacy import (
    RESOURCE_OPTIONS,
)
import json
import os
from typing import (
    Dict,
    List,
    Union,
)

INTEGRATES_TABLE: str = "integrates"
ORGANIZATIONS_TABLE: str = "fi_organizations"
PROJECTS_TABLE: str = "FI_projects"
STAGE: str = os.environ["STAGE"]
USERS_TABLE: str = "FI_users"


async def dynamo_async_scan(
    table: str, scan_attrs: Dict[str, Union[Attr, str]]
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


async def get_all_organizations() -> List[Dict[str, str]]:
    # pylint: disable=unsubscriptable-object
    orgs: List[Dict[str, str]] = []
    scan_attrs: Dict[str, Union[Attr, str]] = {
        "FilterExpression": (
            Attr("pk").begins_with("ORG#") & Not(Attr("sk").contains("#"))
        ),
        "ProjectionExpression": "pk, sk",
    }
    response_items = await dynamo_async_scan(INTEGRATES_TABLE, scan_attrs)
    if response_items:
        orgs = response_items
    return orgs


async def get_organization_groups(org_id: str) -> List[str]:
    # pylint: disable=unsubscriptable-object
    groups: List[str] = []
    scan_attrs: Dict[str, Union[Attr, str]] = {
        "FilterExpression": Attr("organization").eq(org_id),
        "ProjectionExpression": "project_name",
    }
    response_items = await dynamo_async_scan(PROJECTS_TABLE, scan_attrs)
    if response_items:
        groups = [item["project_name"] for item in response_items]
    return groups


async def get_organiation_users(org_id: str) -> List[str]:
    # pylint: disable=unsubscriptable-object
    users: List[str] = []
    scan_attrs: Dict[str, Union[Attr, str]] = {
        "FilterExpression": Attr("organization").eq(org_id),
        "ProjectionExpression": "email",
    }
    response_items = await dynamo_async_scan(USERS_TABLE, scan_attrs)
    if response_items:
        users = [item["email"] for item in response_items]
    return users


async def log(message: str) -> None:
    print(message)
    if STAGE != "test":
        await in_thread(bugsnag.notify, Exception(message), severity="info")


async def main() -> None:
    await log("Starting migration 0014")
    for organization in await get_all_organizations():
        groups = await get_organization_groups(organization["pk"])
        users = await get_organiation_users(organization["pk"])
        items_to_write = [
            {"pk": organization["pk"], "sk": f'INFO#{organization["sk"]}'}
        ]
        if groups:
            items_to_write.extend(
                [
                    {"pk": organization["pk"], "sk": f"GROUP#{group}"}
                    for group in groups
                ]
            )
        if users:
            items_to_write.extend(
                [
                    {"pk": organization["pk"], "sk": f"USER#{user}"}
                    for user in users
                ]
            )
        if STAGE == "test":
            await log(
                f'----\nOrganization {organization["sk"]} with ID '
                f'{organization["pk"]} will have the following records:'
            )
            for item in items_to_write:
                await log("\t" + json.dumps(item))
        else:
            async with aioboto3.resource(
                **RESOURCE_OPTIONS
            ) as dynamodb_resource:
                table = await dynamodb_resource.Table(ORGANIZATIONS_TABLE)
                try:
                    async with table.batch_writer() as batch:
                        for item in items_to_write:
                            await batch.put_item(Item=item)
                except ClientError:
                    await log(
                        f"An error ocurred while updating organization"
                        f'{organization["sk"]} with ID {organization["pk"]}'
                    )
            await log(
                f'----\nOrganization {organization["sk"]} with ID '
                f'{organization["pk"]} was updated as follows:'
            )
            for item in items_to_write:
                await log("\t" + json.dumps(item))


if __name__ == "__main__":
    run(main())
