#!/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration adds an organzation-level customer rule to every member
of an organization

Execution Time: 2020-07-08 16:00:00 UTC-5
Finalization Time: 2020-07-08 17:00:00 UTC-5
"""
import asyncio
import os
from typing import (
    Any,
    Dict,
    List
)

import aioboto3
from aioextensions import in_thread
from boto3.dynamodb.conditions import Attr

from backend import authz
from backend.dal.helpers import dynamodb
from backend.domain import organization as org_domain
from backend.typing import Organization as OrganizationType


RESOURCE_OPTIONS = dynamodb.RESOURCE_OPTIONS
STAGE: str = os.environ['STAGE']
TABLE_NAME: str = 'fi_organizations'


async def dynamo_async_scan(
    table:str,
    scan_attrs: Dict[str, Attr]
) -> List[Any]:
    response_items: List[Any] = []
    async with aioboto3.resource(**RESOURCE_OPTIONS) as dynamodb_resource:
        dynamo_table = await dynamodb_resource.Table(table)
        response = await dynamo_table.scan(**scan_attrs)
        response_items += response.get('Items', [])
        while response.get('LastEvaluatedKey'):
            scan_attrs.update({
                'ExclusiveStartKey': response.get('LastEvaluatedKey')
            })
            response = await dynamo_table.scan(**scan_attrs)
            response_items += response['Items']
    return response_items


async def get_all_organization_users() -> List[OrganizationType]:
    organization_users: List[OrganizationType] = []
    scan_attrs: Dict[str, Attr] = {
        'FilterExpression': Attr('sk').begins_with('USER#')
    }
    items = await dynamo_async_scan(TABLE_NAME, scan_attrs)
    if items:
        organization_users = items
    return organization_users


async def log(message: str) -> None:
    print(message)


async def main() -> None:
    await log('Starting migration 0019')
    for org_user in await get_all_organization_users():
        organization_id: str = str(org_user['pk'])
        user_email: str = str(org_user['sk']).split('#')[1]
        organization_name = await org_domain.get_name_by_id(organization_id)
        if STAGE == 'test':
            await log(
                f'User {user_email} will be added as customer in '
                f'organization {organization_name}'
            )
        else:
            await in_thread(
                authz.grant_organization_level_role,
                user_email,
                organization_id,
                'customer'
            )
            await log(
                f'User {user_email} was given customer role to '
                f'{organization_name}'
            )


if __name__ == '__main__':
    asyncio.run(main())
