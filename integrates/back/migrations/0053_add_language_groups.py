# /usr/bin/env python3
# pylint: disable=invalid-name
"""
This migration adds the attribute "language" to all groups

Execution Time: 2021-01-05 22:14 UTC-5
Finalization Time: 2021-01-05 22:18 UTC-5
"""

import aioboto3
from aioextensions import (
    run,
)
from custom_types import (
    Group as ProjectType,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from groups.dal import (
    TABLE_NAME as GROUPS_TABLE,
)
from typing import (
    List,
)


async def get_groups_without_language() -> List[ProjectType]:
    scan_attrs = {
        "FilterExpression": "attribute_not_exists(#lang)",
        "ExpressionAttributeNames": {"#lang": "language"},
        "ProjectionExpression": "project_name",
    }

    items: List[ProjectType] = []
    async with aioboto3.resource(**dynamodb_ops.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(GROUPS_TABLE)
        response = await table.scan(**scan_attrs)
        items = response.get("Items", [])
        while "LastEvaluatedKey" in response:
            scan_attrs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
            response = await table.scan(**scan_attrs)
            items += response.get("Items", [])
    return items


async def main() -> None:
    groups = await get_groups_without_language()
    print(f"[INFO] Found {len(groups)} groups")

    for group in groups:
        group_name = group["project_name"]
        print(f"Adding languge attribute to group {group_name}...")

        # 'language' is a reserved keyword for the DynamoAPI, so the
        # usual update function does not work
        await dynamodb_ops.update_item(
            GROUPS_TABLE,
            {
                "Key": {"project_name": group_name},
                "UpdateExpression": "SET #lang = :value",
                "ExpressionAttributeValues": {":value": "es"},
                "ExpressionAttributeNames": {"#lang": "language"},
            },
        )


if __name__ == "__main__":
    run(main())
