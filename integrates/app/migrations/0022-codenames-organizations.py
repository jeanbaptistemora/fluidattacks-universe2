#/usr/bin/env python3
#-.- coding: utf-8 -.-
"""
This migration changes the plain name of the organizations for a codename.

Execution Time: 2020-07-17 21:20:00 UTC-5
Finalization Time: 2020-07-17 21:40:00 UTC-5
"""
import os
from typing import (
    Any,
    Dict,
    List
)

import aioboto3
from aioextensions import run
from boto3.dynamodb.conditions import Attr

from backend.dal.helpers import dynamodb
from backend.domain import organization as org_domain
from backend.typing import DynamoDelete as DynamoDeleteType


STAGE: str = os.environ['STAGE']
ORGANIZATION_TABLE = 'fi_organizations'
PORTFOLIO_TABLE = 'fi_portfolios'
RESOURCE_OPTIONS = dynamodb.RESOURCE_OPTIONS
ORGANIZATION_CODENAME_MAP: Dict[str, str] = {
    # Fill this dictionary with keys in the following syntax:
    #     old_name: new_name
}


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


async def main() -> None:
    async for org_id, org_name in org_domain.iterate_organizations():
        if org_name in ORGANIZATION_CODENAME_MAP:
            new_org_name = ORGANIZATION_CODENAME_MAP[org_name].lower()
            new_item: Dict[str, str] = {
                'pk': org_id,
                'sk': f'INFO#{new_org_name}'
            }
            delete_item = DynamoDeleteType(
                Key={
                    'pk': org_id,
                    'sk': f'INFO#{org_name}'
                }
            )
            portfolio_attrs = {
                'FilterExpression': Attr('organization').eq(org_name)
            }
            portfolio_items = await dynamo_async_scan(
                PORTFOLIO_TABLE, portfolio_attrs
            )
            portfolio_keys = []
            for item in portfolio_items:
                portfolio_keys.append(
                    DynamoDeleteType(
                        Key={
                            'organization': item['organization'],
                            'tag': item['tag']
                        }
                    )
                )
                item.update({
                    'organization': new_org_name
                })
            if STAGE == 'test':
                print(f'''
                    -----
                    Organization {org_name}:
                        The following record will be created:
                            {new_item}
                        The following record will be deleted:
                            {delete_item}
                ''')
                for index, item in enumerate(portfolio_items):
                    print(f'''
                            The following portfolio will be created:
                                {item}
                            The following portfolio will be deleted:
                                {portfolio_keys[index]}
                    ''')
            else:
                await dynamodb.async_put_item(ORGANIZATION_TABLE, new_item)
                await dynamodb.async_delete_item(ORGANIZATION_TABLE, delete_item)
                for index, item in enumerate(portfolio_items):
                    await dynamodb.async_put_item(PORTFOLIO_TABLE, item)
                    await dynamodb.async_delete_item(
                        PORTFOLIO_TABLE, portfolio_keys[index]
                    )


if __name__ == '__main__':
    run(main())
