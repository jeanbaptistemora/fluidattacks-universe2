# /usr/bin/env python3
"""
This migration adds the attribute "language" to all groups

Execution Time: 2021-01-05 22:14 UTC-5
Finalization Time: 2021-01-05 22:18 UTC-5
"""
# Standard
import os
import urllib
from typing import List

# Third party
import aioboto3
from aioextensions import run

# Local
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.dal import project as project_dal
from backend.dal.helpers import dynamodb
from backend.typing import Project as ProjectType


async def get_groups_without_language() -> List[ProjectType]:
    scan_attrs = {
        'FilterExpression': 'attribute_not_exists(#lang)',
        'ExpressionAttributeNames': {
            '#lang': 'language'
        },
        'ProjectionExpression': 'project_name'
    }

    items: List[ProjectType] = []
    async with aioboto3.resource(**dynamodb.RESOURCE_OPTIONS) as resource:
        table = await resource.Table(project_dal.TABLE_NAME)
        response = await table.scan(**scan_attrs)
        items = response.get('Items', [])
        while 'LastEvaluatedKey' in response:
            scan_attrs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = await table.scan(**scan_attrs)
            items += response.get('Items', [])
    return items


async def main() -> None:
    groups = await get_groups_without_language()
    print(f'[INFO] Found {len(groups)} groups')

    for group in groups:
        group_name = group['project_name']
        print(f'Adding languge attribute to group {group_name}...')

        # 'language' is a reserved keyword for the DynamoAPI, so the
        # usual update function does not work
        await dynamodb.async_update_item(
            project_dal.TABLE_NAME,
            {
                'Key': {
                    'project_name': group_name
                },
                'UpdateExpression': 'SET #lang = :value',
                'ExpressionAttributeValues': {
                    ':value': 'es'
                },
                'ExpressionAttributeNames': {
                    '#lang': 'language'
                }
            }
        )


if __name__ == '__main__':
    run(main())
