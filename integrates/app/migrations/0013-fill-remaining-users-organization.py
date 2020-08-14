#!/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration aims to fill the organization field for users that do not have
company field or that auto-enrolled to the application.
It will accomplish this by using the organization of the groups these users
have access to.
"""
import asyncio
import os
from typing import (
    Dict,
    List,
    Union
)

import aioboto3
import bugsnag
from asgiref.sync import sync_to_async
from boto3.dynamodb.conditions import Attr, Not

from backend.dal.helpers import dynamodb
from backend.dal.organization import (
    get_by_id as get_organization_attributes,
    get_by_id_old as get_organization_attributes_old
)
from backend.dal.user import update as update_user
from backend.domain.project import get_attributes as get_project_attributes
from backend.domain.organization import (
    get_id_by_name as get_organization_id_by_name
)
from backend.domain.user import get_projects as get_user_projects
from __init__ import FI_COMMUNITY_PROJECTS


AUTOENROLLED_ORGANIZATION: str = 'integrates community'
RESOURCE_OPTIONS: str = dynamodb.RESOURCE_OPTIONS
STAGE: str = os.environ['STAGE']
USERS_TABLE: str = 'FI_users'


async def dynamo_async_scan(
    table:str,
    scan_attrs: Dict[str,Union[Attr, str]]
) -> List[Dict[str, str]]:
    response_items: List[Dict[str, str]] = []
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


async def get_autoenrolled_users() -> List[str]:
    users: List[str] = []
    autoenrolled_org_id: str = await get_organization_id_by_name(
        AUTOENROLLED_ORGANIZATION
    )
    scan_attrs: Dict[str, Union[Attr, str]] = {
        'FilterExpression': Attr('organization').eq(autoenrolled_org_id),
        'ProjectionExpression': 'email'
    }
    response_items = await dynamo_async_scan(USERS_TABLE, scan_attrs)
    if response_items:
        users = [item['email'] for item in response_items]
    return users


async def get_users_without_organization() -> List[str]:
    users: List[str] = []
    scan_attrs: Dict[str, Union[Attr, str]] = {
        'FilterExpression': Not(Attr('organization').exists()),
        'ProjectionExpression': 'email'
    }
    response_items = await dynamo_async_scan(USERS_TABLE, scan_attrs)
    if response_items:
        users = [item['email'] for item in response_items]
    return users


async def log(message: str) -> None:
    print(message)
    if STAGE != 'test':
        await sync_to_async(bugsnag.notify)(Exception(message), 'info')


async def main() -> None:
    await log('Starting migration 0013')
    users_without_org: List[str] = await get_users_without_organization()
    autoenrolled_users: List[str] = await get_autoenrolled_users()
    for user in users_without_org + autoenrolled_users:
        projects: List[str] = await get_user_projects(user)
        projects = list(
            filter(
                lambda project: project not in FI_COMMUNITY_PROJECTS,
                projects
            )
        )
        if not projects:
            await log(
                f'----\nUser {user} does not have access to any projects and '
                f'cannot be associated to any organization'
            )
            continue
        org_info: Dict[str, str] = await sync_to_async(get_project_attributes)(
            projects.pop(0),
            ['organization']
        )
        org_id: str = org_info['organization']
        org_name: Dict[str, str] = await get_organization_attributes_old(org_id, ['name'])
        if not org_name.get('name'):
            org_name = await get_organization_attributes(org_id, ['name'])
        if STAGE == 'test':
            await log(
                f'----\nUser {user} will be added to the organization '
                f'{org_name.get("name")} with ID {org_id}'
            )
        else:
            await sync_to_async(update_user)(
                email=user,
                data={'organization': org_id}
            )
            await log(
                f'User {user} was added to organization '
                f'{org_name.get("name")}'
            )


if __name__ == '__main__':
    asyncio.run(main())
